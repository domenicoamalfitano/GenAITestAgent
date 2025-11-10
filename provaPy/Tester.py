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

# from langchain_ollama import OllamaLLM
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from pathlib import Path
import glob, os, time, subprocess, re
from pathlib import Path
from langchain_groq import ChatGroq

BASE_DIR = Path(__file__).parent.resolve()
JAVA_PROJECT_DIR = BASE_DIR.parent.resolve() / "ProgettoJava"
MAIN_JAVA_DIR = JAVA_PROJECT_DIR / "src" / "main" / "java" / "com" / "example"
TEST_JAVA_DIR = JAVA_PROJECT_DIR / "src" / "test" / "java" / "com" / "example"
SIGNATURES_DIR = BASE_DIR / "signatures"
PROMPT_TEST = "PromptTest.txt"
PROMPT_SOURCE = "PromptSource.txt"
MAX_TEST_RETRIES = 10
MAX_SOURCE_RETRIES = 6
GROQ_API_KEY = "GROQ_API_KEY"
MODEL_LLM = "openai/gpt-oss-120b"
TEMPERATURE = 0.0
MAX_ITERATIONS_TEST = 3
MAX_ITERATIONS_SOURCE = 3


class AgentInvokeError(Exception): # exception of the agent invoke
    pass

    
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
            # if line.strip().startswith("Tests in error:") or line.strip().sta
        if not test_summary:
            test_summary = "Nessun riepilogo dei test trovato nell'output di Maven."
        if "BUILD SUCCESS" in output:
            finals_status = "===RUN_RESULT:BUILD_SUCCESS==="
        else:
            finals_status = "===RUN_RESULT:BUILD_FAIL==="
        return f"{finals_status}\nExit code: {result.returncode}\n{test_summary}\n\nOutput completo:\n{output}"

    except subprocess.TimeoutExpired:
        return "Errore: Il comando Maven ha superato il timeout di 120 secondi."
    except FileNotFoundError:
        return "Errore: Maven non è installato o non è nel PATH."
    except Exception as e:
        return f"Errore durante l'esecuzione di Maven: {str(e)}"

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

def load_llm():
    try:
        # llm = OllamaLLM(model="llama3", temperature=0.0)
        llm =ChatGroq(model=MODEL_LLM, api_key=os.environ.get(GROQ_API_KEY), temperature=TEMPERATURE)
        print("✅ Modello LLM caricato correttamente.")
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

def load_signature_files():
    signature_files = []
    files_path_source = ""
    for filename in glob.glob(str(SIGNATURES_DIR / "*.txt")):
        sig_name = Path(filename).stem
        signature_files.append(filename)
        files_path_source += f"{(str)(MAIN_JAVA_DIR/sig_name)}.java, "
        
    return signature_files, files_path_source

# read a line from file signature and set description if it is necessary
def read_signatures(sig_file):
    with open(sig_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    methods = []
    i = 0
    # call generate_tests_for_method for each method signature in the file
    while i < len(lines):
        # check if the method has a description
        if lines[i].startswith("#"):
            method_description = lines[i][1:].strip()
            method_signature = lines[i+1] if i+1 < len(lines) else None
            i += 2
        else:
            method_description = ""
            method_signature = lines[i]
            i += 1
        if method_signature:
            methods.append((method_signature, method_description))
    return methods

# generation of tests and source for a method, (TDD)
def process_method(method_signature, method_description, class_name, files_path_source, agent_executor_test, agent_executor_source):
    result_test = ""
    attempt = 0
    test_file = str(TEST_JAVA_DIR / f"{class_name}Test.java")
    source_file = str(MAIN_JAVA_DIR / f"{class_name}.java")
    print(f"Generation tests/source for {method_signature}\n")
    
    while "✅ enough tests" not in result_test and attempt < MAX_TEST_RETRIES:
        # generate a single test for the method
        
        print("Generating test...")
        result_test = generate_tests_or_source_for_method(method_signature, method_description, class_name, test_file, PROMPT_TEST, agent_executor_test)
        print(f"Test generation result:\n{result_test[:200]}\n")
        
        # generate/update source code until all tests pass.
        attempt_source = 0
        result_source = ""
        while "✅ All tests passed successfully." not in result_source and attempt_source < MAX_SOURCE_RETRIES:
            print(f"Source fix...")
            result_source = generate_tests_or_source_for_method(method_signature, method_description, class_name, source_file, PROMPT_SOURCE, agent_executor_source, files_path_source)
            attempt_source += 1
            time.sleep(0.3)
                    
        attempt += 1
        time.sleep(0.3)

# function to generate tests for a method or methods for source code
def generate_tests_or_source_for_method(method_signature: str, method_description: str, className: str, file_path: str, promptFile: str, agent_executor: AgentExecutor, files_path_source: str = "") -> str:

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
    prompt=template.format(method_signature=method_signature, method_description=method_description, file_path=file_path, files_path_source=files_path_source, tests=tests, source=source, class_name=className)

    try:
        result = agent_executor.invoke({"input": prompt})
        if not isinstance(result, dict) or "output" not in result:
            raise AgentInvokeError("Output non valido dell'agente")
        return result["output"]
    except Exception as e:
        raise AgentInvokeError(f"Errore durante l'esecuzione dell'agente: {str(e)}")


if __name__ == "__main__":
    TEST_JAVA_DIR.mkdir(parents=True, exist_ok=True)
    MAIN_JAVA_DIR.mkdir(parents=True, exist_ok=True)
    
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
            name="run_maven_test",
            func=run_maven_test,
            description="Esegue i test JUnit in un progetto Maven e restituisce un riepilogo."
        )
    ]

    llm = load_llm()

    prompt_test = return_template_for_test_or_code("test")
    prompt_source = return_template_for_test_or_code("source")

    print("✅ Prompt template creato")
    
    agent_executor_test = create_agent_executor(llm, tools_test, prompt_test, MAX_ITERATIONS_TEST)
    agent_executor_source = create_agent_executor(llm, tools_source, prompt_source, MAX_ITERATIONS_SOURCE)


    print("🚀 Avvio generazione test automatica...")
    # read all signature files
    signature_files, files_path_source = load_signature_files()              
    
    for sig_file in signature_files:

        methods = read_signatures(sig_file)
        class_name = Path(sig_file).stem
        # open signature file and read method signatures with optional description
        
        for method_signature, method_description in methods:     
            try:
                process_method(method_signature, method_description, class_name, files_path_source, agent_executor_test, agent_executor_source)
            except AgentInvokeError as e:
                print(e)
            