from typing import TypedDict, Literal, Annotated
import warnings
import os

warnings.filterwarnings("ignore", category=UserWarning)
os.environ["PYTHONWARNINGS"] = "ignore"

from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

# Tools Import
from tools.parc import weather_tool
from tools.historical_tool import history_tool
from tools.locationn_tool import weather_output
from weather_rag.rag_pipeline.rag_pipeline import build_pipeline

tools = [
    history_tool,
    weather_output,
    weather_tool
]

class Router(BaseModel):
    route: Literal["RAG", "TOOL"]

class AgentState(TypedDict):
    input_message: str
    route: str
    messages: Annotated[list, add_messages]
    answer: str

agent_model = ChatOllama(
    model="llama3.2:3b",
    base_url="http://127.0.0.1:11434",
    temperature=0.3
)

llm_tool_model = agent_model.bind_tools(tools)

def suggestion_node(state: AgentState):
    question = state["input_message"]

    prompt = [
        SystemMessage(
            content="""You are a routing classifier. Classify the user question into "TOOL" or "RAG".
- Choose TOOL if the question is about weather, temperature, rain, forecast, past/historical days, or live alerts.
- Choose RAG if the question is about government schemes, insurance guidelines, policy rules, or documents.

Respond ONLY with TOOL or RAG."""
        ),
        HumanMessage(content=question)
    ]

    response = agent_model.invoke(prompt)
    raw_text = response.content.strip().upper()

    if "TOOL" in raw_text:
        route = "TOOL"
    elif "RAG" in raw_text:
        route = "RAG"
    else:
        route = "TOOL" if any(w in question.lower() for w in ["weather", "temperature", "rain", "forecast", "days", "climate", "history"]) else "RAG"

    print(f"Selected Route: {route}")
    return {"route": route}

def rag_output(state: AgentState):
    question = state["input_message"]
    docs = build_pipeline(question)
    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = [
        SystemMessage(
            content="""You are a helpful assistant. Answer the user question using ONLY the provided context. Give a clear, direct answer."""
        ),
        HumanMessage(content=f"User Question:\n{question}\n\nContext:\n{context}")
    ]

    result = agent_model.invoke(prompt)
    return {"answer": result.content}

def agent_calling(state: AgentState):
    messages = state["messages"]

    system_instruction = SystemMessage(
        content="""You are a weather agent with access to tools.
Always call the tools directly using the tool calling feature. 
Do not output raw JSON or explain what tool you plan to call in text. 
Execute the tool calls immediately."""
    )

    result = llm_tool_model.invoke([system_instruction] + messages)
    return {"messages": [result]}

def tool_condition(state: AgentState):
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "final_answer"

def final_output(state: AgentState):
    last_message = state["messages"][-1]
    return {"answer": last_message.content}

def condition_method(state: AgentState):
    return "rag" if state["route"] == "RAG" else "tool"

# Workflow Setup
workflow = StateGraph(AgentState)

workflow.add_node("suggestion_node", suggestion_node)
workflow.add_node("rag_output", rag_output)
workflow.add_node("agent_call", agent_calling)
workflow.add_node("tools", ToolNode(tools))
workflow.add_node("final_answer", final_output)

workflow.add_edge(START, "suggestion_node")

workflow.add_conditional_edges(
    "suggestion_node",
    condition_method,
    {
        "rag": "rag_output",
        "tool": "agent_call"
    }
)

workflow.add_edge("rag_output", END)

workflow.add_conditional_edges(
    "agent_call",
    tool_condition,
    {
        "tools": "tools",
        "final_answer": "final_answer"
    }
)

workflow.add_edge("tools", "agent_call")
workflow.add_edge("final_answer", END)

app = workflow.compile()

if __name__ == "__main__":
    question = input("Ask Question: ")
    result = app.invoke(
        {
            "input_message": question,
            "route": "",
            "messages": [HumanMessage(content=question)],
            "answer": ""
        }
    )
    print(f"\nRoute: {result['route']}")
    print(f"\nAnswer: {result['answer']}")