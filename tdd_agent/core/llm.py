#
# Copyright (c) 2025 
# Prof. Domenico Amalfitano and Antonio Giaquinto University of Naples Federico II
# Prof. Filippo Ricca and Carlo Arturo Zecca University of Genoa
#
# This file is part of the GenAITestAgent project.
# Developed as part of a bachelor's theses in Computer Engineering and Computer Science
# under the supervision of Prof. Domenico Amalfitano and Prof. Filippo Ricca
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions
# and limitations under the License.
#

from langchain_groq import ChatGroq
from langchain.agents import create_react_agent, AgentExecutor
import os
from tdd_agent.config import GROQ_API_KEY, MODEL_LLM, TEMPERATURE

# load and return the LLM model using groq
def load_llm():
    try:
        llm =ChatGroq(
            model=MODEL_LLM, 
            api_key=os.environ.get(GROQ_API_KEY), 
            temperature=TEMPERATURE,
        )
        print(f"✅ The LLM model {MODEL_LLM} has been loaded successfully.")
        return llm
    except Exception as e:
        raise RuntimeError(f"❌ Error loading the model: {e}")
        

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