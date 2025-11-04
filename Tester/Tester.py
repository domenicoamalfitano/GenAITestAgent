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

# Tooling & Agent imports
from langchain_ollama import OllamaLLM
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from pathlib import Path
import subprocess


# =============================================
# PATH CONFIGURATION
# =============================================

BASE_DIR = Path(__file__).parent.resolve()
JAVA_PROJECT_DIR = BASE_DIR / "ProgettoJava"
MAIN_JAVA_DIR = JAVA_PROJECT_DIR / "src" / "main" / "java" / "com" / "example"
TEST_JAVA_DIR = JAVA_PROJECT_DIR / "src" / "test" / "java" / "com" / "example"

# Automatically ensure test folder exists
TEST_JAVA_DIR.mkdir(parents=True, exist_ok=True)


# =============================================
# FILE WRITING TOOL
# Receives a string "path|||code", saves the code to a file.
# Restricts saving only inside MAIN or TEST directories.
# =============================================

def write_file(input_str: str) -> str:
    try:
        separator = '|||'
        if separator not in input_str:
            return f"Error: invalid format, separator '{separator}' not found."

        file_path, code = input_str.split(separator, 1)
        path = Path(file_path.strip().strip("'").strip('"')).resolve()
        code = code.strip().rstrip("'").rstrip('"')

        # Constraint: file must be inside allowed directories
        allowed_dirs = [MAIN_JAVA_DIR.resolve(), TEST_JAVA_DIR.resolve()]
        if not any(str(path).startswith(str(d)) for d in allowed_dirs):
            return f"Error: file path is not allowed: {path}"

        # Create folders if missing and write code
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding='utf-8') as f:
            f.write(code.strip())

        return f"Code successfully saved to {path}"
    except Exception as e:
        return f"Error while saving file: {str(e)}"


# =============================================
# MAVEN TEST RUNNER TOOL
# Executes mvn test and returns a summary line
# =============================================

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
            test_summary = "No test summary found in Maven output."

        return f"Exit code: {result.returncode}\n{test_summary}\n\nFull Output:\n{output}"

    except subprocess.TimeoutExpired:
        return "Error: Maven command exceeded 120-second timeout."
    except FileNotFoundError:
        return "Error: Maven not installed or not found in PATH."
    except Exception as e:
        return f"Error during Maven execution: {str(e)}"


# =============================================
# TOOL DEFINITIONS FOR LANGCHAIN AGENT
# =============================================

tools = [
    Tool(
        name="write_file",
        func=write_file,
        description="Saves code into a file. Format: path|||file_content"
    ),
    Tool(
        name="run_maven_tests",
        func=run_maven_test,
        description="Runs JUnit tests in a Maven project and returns a summary."
    )
]

# =============================================
# LOAD LLaMA MODEL
# =============================================

try:
    llm = OllamaLLM(model="llama3", temperature=0.0)
    print("✅ LLaMA model loaded successfully")
except Exception as e:
    print(f"❌ Error loading LLaMA: {e}")
    exit(1)


# =============================================
# PROMPT TEMPLATE FOR CREA-REACTION AGENT
# IMPORTANT: String content is now fully in English
# =============================================

template = """Answer the question at your best, using the following tools:

{tools}

Use this format with NO extra text:

Question:
Thought:
Action: one among these [{tool_names}]
Action Input:
Observation:
(Wait for the observation before continuing. Never repeat the same Action twice unless explicitly required.)
Thought:
If all required actions are done, provide your Final Answer.
Final Answer:


⚠️ IMPORTANT - STRICT RULES:
1. Follow this structure:

EXAMPLE OF TEST FILE:
package com.example;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import static org.junit.jupiter.api.Assertions.*;

public class MyClassTest {{
    // code here
}}

2. Do NOT start with '''
3. Do NOT end with '''
4. Do NOT read the implementation of the method under test
5. NEVER wrap file paths or code inside quotes. Do not start or end Action Input with ' or ".


Start!

Question: {input}
{agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)
print("✅ Prompt template created")

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=3,
    handle_parsing_errors=True
)


# =============================================
# TEST GENERATION METHOD
# Loads Signature.txt + Secondo_Prompt.txt
# Builds prompt and executes agent
# =============================================

def generate_tests_for_method(method_signature: str):
    test_file_path = str(TEST_JAVA_DIR / "MyClassTest.java")
    with open("Second_Prompt.txt", "r", encoding="utf-8") as f:
        template = f.read()
    prompt = template.format(method_signature=method_signature, description=description, test_file_path=test_file_path)
    print(prompt)
    try:
        result = agent_executor.invoke({"input": prompt})
        return result
    except Exception as e:
        return f"Error while running agent: {str(e)}"


# =============================================
# MAIN EXECUTION
# Reads Signature.txt, extracts method signature + description,
# and triggers automatic test generation.
# =============================================

if __name__ == "__main__":
    print("🚀 Starting automatic test generation...")
    with open("Signature.txt", "r") as f:
        method_signature = f.readline()
        description = f.readline()
    result = generate_tests_for_method(method_signature)
