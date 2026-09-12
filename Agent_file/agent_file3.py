from typing import TypedDict, Literal

from pydantic import BaseModel

from langchain_ollama import ChatOllama
from langchain.messages import SystemMessage, HumanMessage

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from Agent_file.ml_agent1 import ml_model
from tools.parc import  weather_tool
from tools.historical_tool import history_tool
from tools.locationn_tool import weather_output
import sys
import warnings


try:
    from multiprocess import resource_tracker
    def fix_stop_locked(self):
        pass
    resource_tracker.ResourceTracker._stop_locked = fix_stop_locked
except Exception:
    pass

# Multiprocess cleanup fix for Python 3.12 on Windows
import os
os.environ["PYTHONWARNINGS"] = "ignore"

"""from tools import (
   # API,
    #alert_tool,
    historical_tool,
    locationn_tool,
    parc
    weather_tool
) """


from weather_rag.rag_pipeline.rag_pipeline import build_pipeline


tools = [
   # API,
   # alert_tool,
   
    history_tool,
    weather_output,
    weather_tool,
    ml_model
]


class Router(BaseModel):
    route: Literal["RAG", "TOOL"]


class AgentState(TypedDict):
    input_message: str
    route: str
    messages: list
    answer: str

agent_model = ChatOllama(
    model="llama3.2:3b",
    base_url="http://127.0.0.1:11434",
    temperature=0.5
)

suggest_model = agent_model.with_structured_output(
    Router
)


llm_tool_model = agent_model.bind_tools(
    tools
)

def suggestion_node(state: AgentState):
    question = state["input_message"]

    prompt = [
        SystemMessage(
            content="""You are a strict routing classifier.

Decide whether the user query requires RAG (stored static documents) or TOOL (real-time weather, flood risk, forecast, live predictions, location lookup).

Rules:
- ANY question about weather, flood prediction, rain, temperature, or location coordinates MUST go to TOOL.
- ANY question in Hindi or Hinglish asking about weather or flood risks MUST go to TOOL.

Answer with ONLY one word: RAG or TOOL."""
        ),
        HumanMessage(content=question)
    ]

    response = agent_model.invoke(prompt)
    raw_text = response.content.strip().upper()

    # Tool triggers
    tool_keywords = [
        "weather", "temperature", "rain", "forecast", "days", "climate",
        "flood", "predict", "prediction", "location", "alert", "humidity"
    ]

    if "TOOL" in raw_text:
        route = "TOOL"
    elif "RAG" in raw_text:
        # Override RAG if a primary weather/flood keyword is explicitly in the prompt
        if any(w in question.lower() for w in tool_keywords):
            route = "TOOL"
        else:
            route = "RAG"
    else:
        route = "TOOL" if any(w in question.lower() for w in tool_keywords) else "RAG"

    print(f"Selected Route: {route}")

    return {
        "route": route
    }

"""
def suggestion_node(state: AgentState):

    question = state["input_message"]

    prompt = [
        SystemMessage(
            content=
You are a routing system.

Decide whether the user's question should be answered
using RAG or TOOL.

Use RAG when the question requires information
from the stored knowledge base.

Use TOOL when the question requires:
- real-time information
- weather information
- location information
- historical weather
- alerts
- API data
- external actions

Return only:

RAG

or

TOOL

        ),
        HumanMessage(
            content=question
        )
    ]

    result = suggest_model.invoke(prompt)

    response = agent_model.invoke(prompt)
    raw_text = response.content.strip().upper()

    # Robust matching
    if "TOOL" in raw_text:
        route = "TOOL"
    elif "RAG" in raw_text:
        route = "RAG"
    else:
        route = "TOOL" if any(w in question.lower() for w in ["weather", "temperature", "rain", "forecast", "days", "climate"]) else "RAG"

    print(f"Selected Route: {route}")

    return {
        "route": route
    }

"""
def rag_output(state: AgentState):

    question = state["input_message"]

    docs = build_pipeline(question)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    prompt = [
        SystemMessage(
            content="""
You are a helpful assistant.

Answer the user's question using the provided context.

Give a clear and detailed answer in simple language.

Do not invent information that is not supported
by the provided context.
"""
        ),
        HumanMessage(
            content=f"""
User Question:

{question}

Context:

{context}
"""
        )
    ]

    result = agent_model.invoke(prompt)

    return {
        "answer": result.content
    }


def agent_calling(state: AgentState):
    messages = state["messages"]
    prompt = [
    SystemMessage(
        content="""You are an intelligent agricultural, weather, and flood prediction assistant.

CRITICAL OPERATIONAL RULES:
- NEVER write Python code, script templates, or markdown code blocks in your responses.
- Always invoke tools directly using function calls. Never reply by saying "I will call the tool".

ROUTING & EXECUTION WORKFLOWS:

1. GENERAL / CURRENT WEATHER:
   - Call `weather_tool(city=...)`.
   - Report temperature, humidity, and wind speed.
   - DO NOT call `ml_model` or discuss flood risks.

2. FLOOD PREDICTION ONLY:
   - Step 1: Call `weather_tool(city=...)` to retrieve coordinates.
   - Step 2: Call `ml_model(latitude=..., longitude=..., day=1)`.
   - Report the predicted flood risk flag and probability.

3. GOVERNMENT GUIDELINES / POLICIES / SCHEMES (RAG ONLY):
   - Example triggers: "government guidelines for crops", "crop advisory", "flood relief scheme".
   - Call `rag_tool(query=...)`.
   - Answer directly using the retrieved document context.

4. CROP ADVISORY & SOWING DECISIONS (HYBRID: TOOL + RAG):
   - Example triggers: "Should I plant crops in Patna?", "Is it safe to sow paddy right now?".
   - Step 1: Call `weather_tool(city=...)` to check current local weather and coordinates.
   - Step 2: Call `ml_model(latitude=..., longitude=..., day=1)` to verify flood risk.
   - Step 3: Call `rag_tool(query="crop advisory guidelines for sowing")` to retrieve official agricultural recommendations.
   - Combine the weather conditions, flood risk probability, and official guidelines to give a clear recommendation to the farmer.

5. HISTORICAL WEATHER:
   - Step 1: Call `weather_tool(city=...)` to get coordinates.
   - Step 2: Call `historical_tool(latitude=..., longitude=..., days=...)`.

Execute tools strictly as outlined above!"""
    )
] + messages

    result = llm_tool_model.invoke(prompt)

    return {"messages": messages + [result]}
def tool_condition(state: AgentState):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return "final_answer"


def final_output(state: AgentState):

    last_message = state["messages"][-1]

    return {
        "answer": last_message.content
    }


def condition_method(state: AgentState):

    route = state["route"]

    if route == "RAG":
        return "rag"

    return "tool"


tool_node = ToolNode(
    tools
)


graph = StateGraph(
    AgentState
)


graph.add_node(
    "suggestion_node",
    suggestion_node
)


graph.add_node(
    "rag_output",
    rag_output
)


graph.add_node(
    "agent_call",
    agent_calling
)


graph.add_node(
    "tools",
    tool_node
)


graph.add_node(
    "final_answer",
    final_output
)


graph.add_edge(
    START,
    "suggestion_node"
)


graph.add_conditional_edges(
    "suggestion_node",
    condition_method,
    {
        "rag": "rag_output",
        "tool": "agent_call"
    }
)


graph.add_edge(
    "rag_output",
    END
)


graph.add_conditional_edges(
    "agent_call",
    tool_condition,
    {
        "tools": "tools",
        "final_answer": "final_answer"
    }
)


graph.add_edge(
    "tools",
    "agent_call"
)


graph.add_edge(
    "final_answer",
    END
)


app = graph.compile()


question = input(
    "Ask Question: "
)


result = app.invoke(
    {
        "input_message": question,
        "route": "",
        "messages": [
            HumanMessage(
                content=question
            )
        ],
        "answer": ""
    }
)


print(
    "\nRoute:",
    result["route"]
)


print(
    "\nAnswer:",
    result["answer"]
)