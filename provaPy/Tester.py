"""
Copyright (c) 2025 Prof. Domenico Amalfitano and Antonio Giaquinto
University of Naples Federico II

This file is part of the GenAITestAgent project.
Developed as part of a bachelor's thesis in Computer Engineering
under the supervision of Prof. Domenico Amalfitano.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at:

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions
and limitations under the License.
"""


from langchain_ollama import OllamaLLM
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from pathlib import Path
import subprocess




BASE_DIR = Path(__file__).parent.resolve()
JAVA_PROJECT_DIR = BASE_DIR / "ProgettoJava"
MAIN_JAVA_DIR = JAVA_PROJECT_DIR / "src" / "main" / "java" / "com" / "example"
TEST_JAVA_DIR = JAVA_PROJECT_DIR / "src" / "test" / "java" / "com" / "example"

TEST_JAVA_DIR.mkdir(parents=True, exist_ok=True)



def write_file(input_str: str) -> str:
    try:
        separator = '|||'
        if separator not in input_str:
            return f"Errore: il formato non è corretto, non è stato trovato il separatore '{separator}'."

        file_path, code = input_str.split(separator, 1)
        path = Path(file_path.strip().strip("'").strip('"')).resolve()
        code = code.strip().rstrip("'").rstrip('"')

        # vincolo: deve stare sotto MAIN_JAVA_DIR o TEST_JAVA_DIR
        allowed_dirs = [MAIN_JAVA_DIR.resolve(), TEST_JAVA_DIR.resolve()]
        if not any(str(path).startswith(str(d)) for d in allowed_dirs):
            return f"Errore: il percorso del file non è consentito {path}"



        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding='utf-8') as f:
            f.write(code.strip())

        return f"Codice salvato correttamente in {path}"
    except Exception as e:
        return f"Errore nel salvare il file: {str(e)}"



def run_maven_test(input_str: str = "") -> str:
    try:
        command = ["mvn", "test", "-DfailIfNoTests=false"]
        result = subprocess.run(
            command,
            cwd=JAVA_PROJECT_DIR,
            capture_output=True,
            text=True,
            timeout=120
        )
        output = result.stdout + result.stderr

        summary_line = "Tests run:"
        test_summary = ""
        for line in output.splitlines():
            if summary_line in line:
                test_summary = line.strip()

        if not test_summary:
            test_summary = "Nessun riepilogo dei test trovato nell'output di Maven."

        return f"Exit code: {result.returncode}\n{test_summary}\n\nOutput completo:\n{output}"

    except subprocess.TimeoutExpired:
        return "Errore: Il comando Maven ha superato il timeout di 120 secondi."
    except FileNotFoundError:
        return "Errore: Maven non è installato o non è nel PATH."
    except Exception as e:
        return f"Errore durante l'esecuzione di Maven: {str(e)}"


tools = [
    Tool(
        name="write_file",
        func=write_file,
        description="Salva codice in un file. Formato: 'percorso_file|||contenuto_codice'"
    ),
    Tool(
        name="run_maven_tests",
        func=run_maven_test,
        description="Esegue i test JUnit in un progetto Maven e restituisce un riepilogo."
    )
]

try:
    llm = OllamaLLM(model="llama3", temperature=0.0)
    print("✅ Modello LLaMA caricato correttamente")
except Exception as e:
    print(f"❌ Errore nel caricare LLaMA: {e}")
    exit(1)


template = """Answer the question at your best, use the following tools:

{tools}

Use this format, with no extra text:

Question:
Thought:
Action: one among these [{tool_names}]
Action Input:
Observation:
(Wait for the observation before continuing. Never repeat the same Action twice unless explicitly required.)
Thought:
If all required actions have been completed, provide your Final Answer.
Final Answer:


⚠️ IMPORTANT - STRICT RULES:
1. Follow the following structure:

EXAMPLE OF TEST FILE:
package com.example;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import static org.junit.jupiter.api.Assertions.*;

public class MyClassTest {{
    // code  here
}}

2. Don't start with '''
3. Don't end with '''
4. Don't read the implementation of the method under test
5. Never enclose file paths or code inside quotes. Do not start or end Action Input with ' or ".






Start!

Question: {input}
{agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)
print("✅ Prompt template creato")

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=3,
    handle_parsing_errors=True
)


def generate_tests_for_method(method_signature: str):
    test_file_path = str(TEST_JAVA_DIR / "MyClassTest.java")
    with open("Prompt.txt","r",encoding="utf-8") as f:
        template=f.read()
    prompt=template.format(method_signature=method_signature,test_file_path=test_file_path)
    print(prompt)
    try:
        result = agent_executor.invoke({"input": prompt})
        return result
    except Exception as e:
        return f"Errore durante l'esecuzione dell'agente: {str(e)}"


if __name__ == "__main__":
    print("🚀 Avvio generazione test automatica...")
    with open("Signature.txt","r") as f:
        method_signature = f.readline()
        #description=f.readline()
    result = generate_tests_for_method(method_signature)



