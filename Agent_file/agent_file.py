"""from langchain_ollama import ChatOllama
import os
import json 
from typing import TypedDict
from langgraph.graph import StateGraph , START,END
from tools import API,alert_tool,historical_tool,locationn_tool,parc,weather_tool
from pydantic import typing,Typedict
from langchain.messages import SystemMessage,AIMessage,HumanMessage
from langchain_core.tools import tool
from weather_rag\rag_pipeline\rag_pipeline import build_pipeline
tools=[API,alert_tool,historical_tool,locationn_tool,parc,weather_tool]
# Make pydantic 


class agentState(Typedict):
    message:str


    agent_model=ChatOllama(
    model="ollama-3.12b"
    temperature=0.5
    )
    llm_tool=agent_model.bind_tools(tools)
    def talking_method(state:agentState):
         work like a agent when tool needed then answer other wise
          do not answer like and 
        if some one ask from guide line etc type question
          then use this other wise do not use this 
        
        prompt={
           SystemMessage(
               " You are a ai agent work like a ai agent when we ask question related " \
               "to tool calling then give me answer via it other wise give direct answer using your mind " \
               " also if some one agk question on  some guideline, " \
               " method u can use rag based dystem to answer and explain in simple easy way"
               " and give answer propelly"
           ),
           HumanMessage(
               f"The question is given give answer in proper way in details in simple from the question is given below {question} "
        
           )
          {"question":question}
        }
    def condition_approch(state:agentState):
        message =state["message"]
        if "tool_calling" in message:
            return (
                ""
            )

graph=StateGraph(agentState)
graph.add_node("agentic_rag",build_pipeline)
graph.add_node("talking_method",talking_method)
graph.add_edge(START,"talking_method")
graph.add_edge("talking_method",END)
app=graph.compile()
enter_question=input("Ask The question:")
output_answer=app.invoke(enter_question)
print(output_answer)
# app.invoke wala
# agent_node for rag or node
rout_question mein rag ya tool aaayenga 
# rag node mein agr rag aaya to aasa banayenge ontext = "\n\n".join(
        doc.page_content
        for doc in documents
    )
agar tool_node aaya to tool node iundera # make agent mode and tool node diff

            HumanMessage(
                content=question
            )


route = response.content.strip().upper()

    if route not in ["RAG", "TOOL"]:
        route = "RAG"

    print(f"Selected route: {route}")

    return {
        "question": question,
        "route": route,
        "answer": ""
    }

 """