"""from typing import TypedDict, Literal

from pydantic import BaseModel

from langchain_ollama import ChatOllama
from langchain.messages import SystemMessage, HumanMessage

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from tools import (
    API,
    alert_tool,
    historical_tool,
    locationn_tool,
    parc
    #weather_tool
)


from weather_rag.rag_pipeline.rag_pipeline import build_pipeline


tools = [
    API,
    alert_tool,
    historical_tool,
    locationn_tool,
    parc,
    #weather_tool
]


class Router(BaseModel):
    route: Literal["RAG", "TOOL"]


class AgentState(TypedDict):
    input_message: str
    route: str
    messages: list
    answer: str


agent_model = ChatOllama(
    model="llama3.2:12b",
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

    route = result.route.upper()

    if route not in ["RAG", "TOOL"]:
        route = "RAG"

    print(f"Selected route: {route}")

    return {
        "route": route
    }


def rag_output(state: AgentState):

    question = state["input_message"]

    docs = build_pipeline(question)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    prompt = [
        SystemMessage(
            content=
You are a helpful assistant.

Answer the user's question using the provided context.

Give a clear and detailed answer in simple language.

Do not invent information that is not supported
by the provided context.

        ),
        HumanMessage(
            content=f
User Question:

{question}

Context:

{context}

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
            content=
You are an intelligent weather assistant.

Use the available tools whenever they are required
to answer the user's question.

If a tool gives information required by another tool,
use the result of the first tool to call the next tool.

For example:

If the user asks for historical weather of a city:

1. Use weather_tool to get latitude and longitude.

2. Use historical_tool using the latitude,
   longitude and required number of days.

Continue using tools until you have enough information
to answer the user's question.

Give the final answer in simple and clear language.

        )
    ] + messages

    result = llm_tool_model.invoke(prompt)

    return {
        "messages": messages + [result]
    }


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
) """