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
import glob, os, re
from pathlib import Path
from langchain_groq import ChatGroq



BASE_DIR = Path(__file__).parent.resolve()
JAVA_PROJECT_DIR = BASE_DIR.parent.resolve() / "ProgettoJava"
MAIN_JAVA_DIR = JAVA_PROJECT_DIR / "src" / "main" / "java" / "com" / "example"
TEST_JAVA_DIR = JAVA_PROJECT_DIR / "src" / "test" / "java" / "com" / "example"
PROMPT_TEST = "Prompt2.txt"
PROMPT_SOURCE = "PromptSource2.txt"

TEST_JAVA_DIR.mkdir(parents=True, exist_ok=True)

class AgentInvokeError(Exception): # exception of the agent invoke
    pass

# take only the code into a class/ test class
    
def write_file_truncate(input_str: str) -> str:
    try:
        separator = '|||'
        if separator not in input_str:
            return f"Errore: il formato non è corretto, non è stato trovato il separatore '{separator}'."

        file_path, code = input_str.split(separator, 1)
        path = Path(file_path.strip().strip("'").strip('"')).resolve()
        code = code.strip().rstrip("'").rstrip('"').replace("```","").replace("<complete code here>","").strip()

        # vincolo: deve stare sotto MAIN_JAVA_DIR o TEST_JAVA_DIR
        allowed_dirs = [MAIN_JAVA_DIR.resolve(), TEST_JAVA_DIR.resolve()]
        if not any(str(path).startswith(str(d)) for d in allowed_dirs):
            return f"Errore: il percorso del file non è consentito {path}"

        path.parent.mkdir(parents=True, exist_ok=True)
        # If the file exists, read its content and append only the new test methods
                 
        with path.open("w", encoding='utf-8') as f:
            f.write(code.strip())

        return f"Codice salvato correttamente in {path}"
    except Exception as e:
        return f"Errore nel salvare il file: {str(e)}"


def run_maven_test(input_str: str = "") -> str:
    try:
        mvn_exe = r"C:\apache-maven-3.9.11\bin\mvn.cmd"
        command = [mvn_exe, "test", "-DfailIfNoTests=false"]
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


tools_test = [
    Tool(
        name="write_file_truncate",
        func=write_file_truncate,
        description="Salva codice in un file. Formato: 'percorso_file|||contenuto_codice'"
    )
]

tools_source = [
    Tool(
        name="write_file_truncate",
        func=write_file_truncate,
        description="Salva codice in un file. Formato: 'percorso_file|||contenuto_codice'"
    ),
    Tool(
        name="run_maven_tests",
        func=run_maven_test,
        description="Esegue i test JUnit in un progetto Maven e restituisce un riepilogo."
    )
]

try:
    # llm = OllamaLLM(model="llama3", temperature=0.0)
    llm =ChatGroq(model="qwen/qwen3-32b", api_key=os.environ.get("GROQ_API_KEY"), temperature=0.0)
    print("✅ Modello LLaMA caricato correttamente")
except Exception as e:
    print(f"❌ Errore nel caricare LLaMA: {e}")
    exit(1)

def return_template_for_test_or_code(typeTemplate: str)-> PromptTemplate:
    if typeTemplate=="test":
        example_block = """1. Follow the following structure for test file:

        EXAMPLE OF TEST FILE:
        package com.example;

        import org.junit.jupiter.api.Test;
        import org.junit.jupiter.api.DisplayName;
        import static org.junit.jupiter.api.Assertions.*;

        public class MyClassTest {{
            
            // code  here
        }}"""
    elif typeTemplate=="source":
        example_block = """1. Follow the following structure for source file:

        EXAMPLE OF SOURCE FILE:
        package com.example;

        public class MyClass {{
            
            // code  here
        }}"""
    else:
        raise ValueError("typeTemplate must be 'test' or 'source'")
    
    template = f"""Answer the question at your best, use the following tools:

    {{tools}}

    Use this format, with no extra text:

    Question:
    Thought:
    Action: one among these [{{tool_names}}]
    Action Input:
    Observation:
    (Wait for the observation before continuing. Never repeat the same Action twice unless explicitly required.)
    Thought:
    If all required actions have been completed, provide your Final Answer:
    Final Answer:


⚠️ IMPORTANT - STRICT RULES:
    {example_block}
        
    2. Don't start with '''
    3. Don't end with '''
    4. Don't read the implementation of the method under test
    5. Never enclose file paths or code inside quotes. Do not start or end Action Input with ' or ".






    Start!

    Question: {{input}}
    {{agent_scratchpad}}
    """
    
    return PromptTemplate.from_template(template)

prompt_test = return_template_for_test_or_code("test")
prompt_source = return_template_for_test_or_code("source")

print("✅ Prompt template creato")

# create and return AgentExecutor
def create_agent_executor(tools, prompt, max_iterations):
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=max_iterations,
        handle_parsing_errors=True
    )
    return agent_executor

agent_executor_test = create_agent_executor(tools_test, prompt_test, 1)
agent_executor_source = create_agent_executor(tools_source, prompt_source, 5)

# function to generate tests for a method or methods for source code
def generate_tests_or_source_for_method(method_signature: str, method_description: str, className: str, file_path: str, promptFile: str, agent_executor: AgentExecutor) -> str:

    tests = ""
    if (TEST_JAVA_DIR / f"{className}Test.java").exists():
        with open(TEST_JAVA_DIR / f"{className}Test.java","r",encoding="utf-8") as f:
            tests = f.read()

    source = ""
    if (MAIN_JAVA_DIR / f"{className}.java").exists():
        with open(MAIN_JAVA_DIR / f"{className}.java", "r", encoding="utf-8") as f:
            source = f.read()
    
    with open(promptFile,"r",encoding="utf-8") as f:
        template=f.read()
    prompt=template.format(method_signature=method_signature, method_description=method_description, file_path=file_path, tests=tests, source=source, class_name=className)
    print(prompt)
    try:
        result = agent_executor.invoke({"input": prompt})
        if not isinstance(result, dict) or "output" not in result:
            raise AgentInvokeError("Output non valido dell'agente")
        return result["output"]
    except Exception as e:
        raise AgentInvokeError(f"Errore durante l'esecuzione dell'agente: {str(e)}")


if __name__ == "__main__":
    print("🚀 Avvio generazione test automatica...")
    # read all signature files
    for filename in glob.glob(str(BASE_DIR / "signatures/*.txt")):
        sigFileName = Path(filename).stem
        os.remove(TEST_JAVA_DIR / f"{sigFileName}Test.java") if (TEST_JAVA_DIR / f"{sigFileName}Test.java").exists() else None
        os.remove(MAIN_JAVA_DIR / f"{sigFileName}.java") if (MAIN_JAVA_DIR / f"{sigFileName}.java").exists() else None

        # open signature file and read method signatures with optional description
        with open(f"{filename}","r") as f:
            lines = [line.strip() for line in f if line.strip()]
        method_signature = ""
        method_description = ""
        i = 0
        # call generate_tests_for_method for each method signature in the file
        while i < len(lines):
            line = lines[i]
            # check if the method has a description
            if line.startswith("#"):
                method_description = line[1:].strip()
                if i+1 < len(lines):
                    method_signature = lines[i+1]
                    i += 2
                else:
                    break
            else:
                method_description = ""
                method_signature = line
                i += 1

            # generate tests for the method
            try:
                result = ""
                max_retries = 12
                attempt = 0
                while "|enough tests|" not in result and attempt < max_retries:
                    file_path = str(TEST_JAVA_DIR / f"{sigFileName}Test.java")
                    result = generate_tests_or_source_for_method(method_signature, method_description, sigFileName, file_path, PROMPT_TEST, agent_executor_test)
                        
                    file_path = str(MAIN_JAVA_DIR / f"{sigFileName}.java")
                    result_source = generate_tests_or_source_for_method(method_signature, method_description, sigFileName, file_path, PROMPT_SOURCE, agent_executor_source)
                    attempt += 1
            except AgentInvokeError as e:
                print(e)
            