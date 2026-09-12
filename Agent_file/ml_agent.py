# NOW start the tool calling fro mhere 
"""mport joblib
import json 
import numpy as np
from langchain_core.tools import tool
model=joblib.load("flood_nodel.pkl")
scaller=joblib.load("flood_scaler.pkl")
from pydantic import BaseModel,Field
from typing import TypedDict
from langchain_ollama import ChatOllama
# Now call the ollama 
# Now answer should me on base model type 
class WorkModel(BaseModel):
    message:str=Field(description="Message should be in percentage ")

model_output=ChatOllama(
    model="3.12b13",
    temperature=0.5
)
model_structure=model_output.with_structured_output(WorkModel)

from langchain.messages import SystemMessage, AIMessage ,ToolMessage,HumanMessage
# Import the tool here 
class message_class(TypedDict):
    message:str
@tool
def ml_tool( humidity,flood,hr_1h, hr_3hr, hr_4hr, flow):
    " generate the answer according to given feedback or return value "
     x=np.array([[
                rainfall_1h_mm,
                rainfall_6h_mm,
                rainfall_24h_mm,
                rainfall_3day_mm,
                temperature,
                humidity,
                pressure,
                wing_speed,
                cloud_cover
        ]]) 
    # use the same name as base name 
    message=WorkModel["message"]
    # Call scatter then check the type
    print("The flood type check is :",type(x))
    scaller_output=scaller.transform(x)
    model_output=model.fit_transform(scaller_output)
    # Now check via using probality
    prob=model_output.predict_prob(model_output)[0][1]
    # Now check the probality according to iy
    output_prob=prob*100
    # Now check via using output prob
    # use prompty type 
    
    prompt=[
         SystemMessage(content="write the output"
              " according to given answer and " \
              "output shopuld be simple and easy in the basic form"
              "  model ashould be easy type  "),
              HumanMessage(content= f"The answer should be in problilty form in simple way and eack answer should be same {output_prob} ")
              
    ]
    model=model.invoke(prompt)
    return {
        message:{
             model
         }
    }
    

# first we call out model here
# Now start making edges and nodes here  just for practices here 
graph=Stategraph(Agentgraph)
# Add nodes '
def suggest_node(state:message_class):
    # check tyhe output 
    message= message_class["message"]
    # check the input and tell given question give tool or rag type so tell me this only 
    prompt=[
        SystemMessage(
            content="Now check from the model and answer give us in the form RAG and tool "
        ), HumanMessage(
            content=f"Now give me the answer according to answer in simple way { message } "
        )
    ]
    output_naswer= model_output.invoke(prompt)
    output_naswer=output_naswer.content.strip().upper()
    if "TOOL" in output_naswer:
        router="TOOL"
    elif "RAG" in output_naswer:
        router="RAG"
    else:
        rotering=["TOOL","WEATHER_TOOL","TOKEN","OUTPUT"]
        if rotering in output_naswer:
            router="TOOL"
    return {
        "router":router
    }
def rag_output(state:AgentNode):
    messaage:state["message"]
    docs=system_output(messaage)
    #context = \n\n.join(
            doc.page_content
            for doc in docs
        )
    
    prompt=[
        SystemMessage(
            content="the output of rah should b e answer accoprding t given "
            ),HumanMessage(
                content=f"The answer should be simple ans easy in simple from {messaage}"
            )
    ]
    model_out=model_output.invoke(prompt)
    return {
        messaage : model_out
    }



graph.add_nodes("suggent_node",suggent_node)

# now made the limited token 
def stage_tool(state: AgentNode):
    message:state["message"]
    prompt=[
        SystemMessage(
            content=" if previes content requided use it and also use other things also accordin to it "
        ), AIMessage(
            content=f"The answer shoul be in smpkle and easy way in details type"
        ) + message 
    ]
    result=model_output.invoke(prompt)
    return {
        "message":prompt + [result]
    }

# Make condition checking it token requided or not 
def condition_tool(state:AgentNode):
    if message.Tool_calling:
        return "tool_call"
    else :
        return "agent_call"
def condition_calling(state:AgentNode):
    round=state["route"]
    if round == "RAG":
        return "rag"
    else:
        return "tools"

# Now just tell me answer 
graph.add_nodes(START, "work")
graph.add_condition_edges(
    "work",condition_calling(
        "rag":"rag_)output",
        "tool":"agent_call"
    )
)
graph.add_condition_edges(
    "tool_calling",
    tool_calling,{
        "tool":"tool_calling"
        "rag":"final answer"
    }
) 
"""