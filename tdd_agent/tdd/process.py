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





from tdd_agent.config import WORKFLOW_LOG
from tdd_agent.core.graph.state import TDDState
from tdd_agent.core.graph.build_graph import build_tdd_graph




# process a method through the TDD phases: RED, GREEN, and REFACTOR
def process_method(
    method_signature: str,
    method_description: str,
    class_name: str,
    files_path_source: str,
    agent_executor_test,
    agent_executor_source,
    agent_executor_refactor,
):
    print(f"Start TDD iteration for:\n{method_signature}\nDescription:\n{method_description}\n")

    with open(WORKFLOW_LOG, "a", encoding="utf-8") as f:
        f.write(f"\n=== TDD Iteration for Method: {method_signature} ===\n")

    initial_state: TDDState = {
        "method_signature": method_signature,
        "method_description": method_description,
        "class_name": class_name,
        "files_path_source": files_path_source,
        "result_test": "",
        "result_source": "",
        "result_refactor": "",
        "attempt_red": 0,
        "attempt_green": 0,
        "attempt_refactor": 0,
        "agent_executor_test": agent_executor_test,
        "agent_executor_source": agent_executor_source,
        "agent_executor_refactor": agent_executor_refactor,
    }

    graph = build_tdd_graph()
    graph.invoke(initial_state)
