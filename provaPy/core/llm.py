from langchain_groq import ChatGroq
from langchain.agents import create_react_agent, AgentExecutor
import os
from config import GROQ_API_KEY, MODEL_LLM, TEMPERATURE

def load_llm():
    try:
        llm =ChatGroq(
            model=MODEL_LLM, 
            api_key=os.environ.get(GROQ_API_KEY), 
            temperature=TEMPERATURE
        )
        print(f"✅ Il modello LLM {MODEL_LLM} è stato caricato correttamente.")
        return llm
    except Exception as e:
        raise RuntimeError(f"❌ Errore nel caricare il modello: {e}")
        

# create and return AgentExecutor
def create_agent_executor(llm, tools, prompt, max_iterations):
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=max_iterations,
        handle_parsing_errors=True
    )
    return agent_executor