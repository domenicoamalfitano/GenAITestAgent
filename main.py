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

from tdd_agent.config import TEST_JAVA_DIR, MAIN_JAVA_DIR, MAX_ITERATIONS, LOGS_DIR, WORKFLOW_LOG, PROMPT_COUNTERS
from tdd_agent.core.tools import write_file_truncate, run_maven_test, read_file
from tdd_agent.core.llm import load_llm, create_agent_executor
from tdd_agent.core.exceptions import AgentInvokeError
from tdd_agent.tdd.signatures import load_signature_files, read_signatures
from tdd_agent.tdd.process import process_method

# from langchain.agents import Tool

from tdd_agent.core.template import return_template_for_test_or_code
from pathlib import Path
from dotenv import load_dotenv
import re, time

load_dotenv('.env')

if __name__ == "__main__":
    start_time = time.perf_counter()# start time measurement

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(WORKFLOW_LOG, "w", encoding="utf-8") as log_main:
        log_main.write(f"=== Workflow Log ===\n\n")
        
    TEST_JAVA_DIR.mkdir(parents=True, exist_ok=True)
    MAIN_JAVA_DIR.mkdir(parents=True, exist_ok=True)
    
    # define the tools
    tools = [
        write_file_truncate,
        run_maven_test,
        read_file
    ]
    tools_RED = tools[:2] # remove read_file tool for RED phase

    # create prompt templates for test and source code generation
    prompt_test = return_template_for_test_or_code("test")
    prompt_source = return_template_for_test_or_code("source")
    print("✅ created prompt templates.")
    
    # load LLM and create agent executors
    llm = load_llm()
    
    # create agent executors for RED, GREEN, and REFACTOR phases
    agent_executor_test = create_agent_executor(llm, tools_RED, prompt_test, MAX_ITERATIONS)
    agent_executor_source = create_agent_executor(llm, tools, prompt_source, MAX_ITERATIONS)
    agent_executor_refactor = create_agent_executor(llm, tools, prompt_source, MAX_ITERATIONS)

    # read all signature files
    signature_files, files_path_source = load_signature_files()          
    if not signature_files:
        print("❌ No signature files found. Exiting.")
        exit(1)
        
    print("🚀 Starting Test Driven Development...")
    for sig_file in signature_files:
        
        with open(WORKFLOW_LOG, "a", encoding="utf-8") as log_main:
            log_main.write(f"- Processing signature file: {sig_file}\n")
        
        # read method signatures from the signature file
        methods = read_signatures(sig_file)
        stem = Path(sig_file).stem
        if re.match(r"^[0-9]+_", stem):
            class_name = re.sub(r"^[0-9]+_", "", stem)
        else:
            class_name = Path(sig_file).stem
        
        # process each method through the TDD phases
        for method_signature, method_description in methods:
            try:
                process_method(method_signature, method_description, class_name, files_path_source, agent_executor_test, agent_executor_source, agent_executor_refactor)
            except AgentInvokeError as e:
                print(e)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    minutes, seconds = divmod(elapsed_time, 60)
    
    end_message = "✅ TDD completed."
    total_num_prompts_message = f"Total prompts invoked - RED: {PROMPT_COUNTERS['RED']}, GREEN: {PROMPT_COUNTERS['GREEN']}, REFACTOR: {PROMPT_COUNTERS['REFACTOR']}\n"
    time_message = f"Total execution time: {int(minutes)} minutes and {seconds:.2f} seconds\n"
    print(end_message + "\n" + total_num_prompts_message + "\n" + time_message)

    with open(WORKFLOW_LOG, "a", encoding="utf-8") as log_main:
        log_main.write(f"\n\n{end_message}\n{total_num_prompts_message}\n{time_message}")
    