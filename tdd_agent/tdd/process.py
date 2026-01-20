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

from tdd_agent.core.exceptions import AgentInvokeError
from langchain.agents import AgentExecutor
import time
from tdd_agent.config import TEST_JAVA_DIR, MAIN_JAVA_DIR, PROMPT_TEST, PROMPT_SOURCE, PROMPT_REFACTOR, RESPONSE_TESTS_ENOUGH, RESPONSE_ALL_TESTS_PASSED, RESPONSE_REFACTORING_COMPLETE, MAX_RETRIES, WORKFLOW_LOG, PROMPT_COUNTERS
from langchain_groq import ChatGroq

# process a method through the TDD phases: RED, GREEN, and REFACTOR
def process_method(method_signature, method_description, class_name, files_path_source, agent_executor_test, agent_executor_source, agent_executor_refactor):
    result_test = ""
    attempt_red = 0
    test_file = str(TEST_JAVA_DIR / f"{class_name}Test.java").replace("\\","/")
    source_file = str(MAIN_JAVA_DIR / f"{class_name}.java").replace("\\","/")
    
    print(f"Start TDD iteration for:\n{method_signature}\nDescription:\n{method_description}\n")
    
    with open(WORKFLOW_LOG, "a", encoding="utf-8") as log_main:
        log_main.write(f"\n=== TDD Iteration for Method: {method_signature} ===\n")
    
    while RESPONSE_TESTS_ENOUGH not in result_test and attempt_red < MAX_RETRIES:
        try:
            # RED PHASE: generate a failed test
            print("RED PHASE...")
            result_test = generate_tests_or_source_for_method(method_signature, method_description, class_name, test_file, PROMPT_TEST, agent_executor_test)
            if RESPONSE_TESTS_ENOUGH in result_test:
                continue
        except AgentInvokeError as e:
            print(f"Error during agent execution in the RED phase: {str(e)}")
            attempt_red += 1
            continue
        # GREEN PHASE: generate/update source code until all tests pass.
        attempt_green = 0
        result_source = ""
        while RESPONSE_ALL_TESTS_PASSED not in result_source and attempt_green < MAX_RETRIES:
            try:
                print(f"GREEN PHASE...")
                result_source = generate_tests_or_source_for_method(method_signature, method_description, class_name, source_file, PROMPT_SOURCE, agent_executor_source, files_path_source)
            except AgentInvokeError as e:
                print(f"Error during agent execution in the GREEN phase: {str(e)}")
                attempt_green += 1
                continue
            
            attempt_green += 1
            time.sleep(0.3)

        # REFACTOR PHASE: improve code structure
        attempt_refactor = 0
        result_refactor = ""
        while (RESPONSE_ALL_TESTS_PASSED not in result_refactor or RESPONSE_REFACTORING_COMPLETE not in result_refactor) and attempt_refactor < MAX_RETRIES:
            try:
                print(f"REFACTOR PHASE...")
                result_refactor = generate_tests_or_source_for_method(method_signature, method_description, class_name, source_file, PROMPT_REFACTOR, agent_executor_refactor, files_path_source)
            except AgentInvokeError as e:
                print(f"Error during agent execution in the REFACTOR phase: {str(e)}")
                attempt_refactor += 1
                continue
            
            attempt_refactor += 1
            time.sleep(0.3)

        attempt_red += 1
        time.sleep(0.3)

def increment_num_invokes_and_return_msg_invoke(promptFile: str):
    if promptFile == PROMPT_TEST:
        namePrompt = "RED phase"
        PROMPT_COUNTERS["RED"] += 1
    elif promptFile == PROMPT_SOURCE:
        namePrompt = "GREEN phase"
        PROMPT_COUNTERS["GREEN"] += 1
    else:
        namePrompt = "REFACTOR phase"
        PROMPT_COUNTERS["REFACTOR"] += 1
    return f"\t --- Invoked {namePrompt}\n"


# build the prompt for RED or GREEN/REFACTOR phase and invoke the agent executor
def generate_tests_or_source_for_method(method_signature: str, method_description: str, className: str, file_path: str, promptFile: str, agent_executor: AgentExecutor, files_path_source: str = "") -> str:
    
    # Build the prompt
    tests = "No tests"
    if (TEST_JAVA_DIR / f"{className}Test.java").exists():
        with open(TEST_JAVA_DIR / f"{className}Test.java","r",encoding="utf-8") as f:
            tests = f.read()
        
    source = "No source"
    if (MAIN_JAVA_DIR / f"{className}.java").exists():
        with open(MAIN_JAVA_DIR / f"{className}.java", "r", encoding="utf-8") as f:
            source = f.read()
    
    with open(promptFile,"r",encoding="utf-8") as f:
        template=f.read()
    prompt=template.format(method_signature=method_signature, method_description=method_description, file_path=file_path, files_path_source=files_path_source, tests=tests, source=source, class_name=className)
    
    # Invoke the agent executor
    try:
        namePrompt = increment_num_invokes_and_return_msg_invoke(promptFile)

        result = agent_executor.invoke({"input": prompt})
        if not isinstance(result, dict) or "output" not in result:
            raise AgentInvokeError("Invalid agent output")
        
        with open(WORKFLOW_LOG, "a", encoding="utf-8") as log_main:
            log_main.write(namePrompt)
        
        return result["output"]
    except Exception as e:
        error_message = f"Error during agent execution: {str(e)}"
        with open(WORKFLOW_LOG, "a", encoding="utf-8") as log_main:
            log_main.write(f"{namePrompt}\t\t {error_message}\n")
        raise AgentInvokeError(f"{error_message}")