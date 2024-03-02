from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import (
    StreamingStdOutCallbackHandler
)
from langchain.tools import StructuredTool

from langchain.agents import AgentExecutor
from langchain.agents import create_json_chat_agent 
from langchain.chains.conversation.memory import ConversationBufferWindowMemory


## Import AI Agent Tools
from tools.image import analyzeImage
from tools.nslookup import nsLookup

## Uncomment the following line to enable debug mode
# import langchain 
# langchain.debug = True


#############################################################
############################ LLM ############################
#############################################################

## Define the LLM (Language Learning Model) to be used, in this case, Ollama server running on localhost
llm = Ollama(base_url="http://localhost:11434", 
            model="codellama", 
            callback_manager = CallbackManager([StreamingStdOutCallbackHandler()]),
            temperature = 0
            )

#############################################################
########################### AGENT ###########################
#############################################################

def agent():
    ## Define the tools which the AI Agent have access to
    tools = [
        StructuredTool.from_function(
            func=nsLookup,
            name="nsLookup",
            #handle_tool_error=errorHandler,
            handle_tool_error="Check your output and make sure it conforms",
            description="Tool that can be used for NS Lookups. \
                With a domain as input, it returns a dictonary containing IP for the domain."
        ),
        StructuredTool.from_function(
            func=analyzeImage,
            name="analyzeImage",
            #handle_tool_error=errorHandler,
            handle_tool_error="Check your output and make sure it conforms",
            description="Tool to analyze an image and return a description \
                of the image in the format of a dictonary. The input must be be a URL to an image. \
                    This tool must not be used if there is not an image url in the request."
        )
    ]
    ## Import the AI Agent Prompt
    from prompt import getAgentPrompt
    agentPrompt = getAgentPrompt()
    #from langchain_core.messages import AIMessage, HumanMessage


    ## Define the memory for chat history to be used by the AI Agent
    memory = ConversationBufferWindowMemory(
        memory_key='chat_history',
        k=5,
        return_messages=True,
    )

    ## Create the AI Agent, using JSON Chat Agent
    agent = create_json_chat_agent(llm, tools, agentPrompt, memory)

    agentExecutor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        handle_parsing_errors=True,
        )
    return agentExecutor

def invokeAgent(prompt: str, chatHistory: list):
    response = agent().invoke(
        {
            "input": prompt,
            "chat_history": chatHistory
        }
            )
    print(f"invokeAgent - Prompt: {prompt} Response: {response}")
    return response

#############################################################
########################### MAIN ############################
#############################################################

if __name__ == "__main__":

    ## Test the AI Agent with some prompts
    prompt = "What is google.com's ip address?"
    invokeAgent(prompt, [])

    imageUrl = "https://images.unsplash.com/photo-1616128417859-3a984dd35f02?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2372&q=80"
    prompt = f"What animal and where is that animal in this image? {imageUrl}"
    invokeAgent(prompt, [])
