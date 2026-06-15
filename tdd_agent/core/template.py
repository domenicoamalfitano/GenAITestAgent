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

from langchain_core.prompts import PromptTemplate

def return_template_for_test_or_code(typeTemplate: str)-> PromptTemplate:
    if typeTemplate=="test":
        example_block = """1. Follow the following structure for test file:

        EXAMPLE OF TEST FILE:
        package com.example;

        import org.junit.jupiter.api.Test;
        import org.junit.jupiter.api.DisplayName;
        import static org.junit.jupiter.api.Assertions.*;

        public class <CLASS_NAME>Test {{
            
            // code here
        }}"""
    elif typeTemplate=="source":
        example_block = """1. Follow the following structure for source file:

        EXAMPLE OF SOURCE FILE:
        package com.example;

        public class <CLASS_NAME> {{
            
            // code here
        }}"""
    else:
        raise ValueError("typeTemplate must be 'test' or 'source'")

    template = f"""You are an expert Java test generator for Maven projects.

You MUST follow strictly the workflow and rules below.

---

### TOOL USAGE
You have access to tools. You MUST use tools when required.
Do NOT simulate tool execution.

Available tools:
{{tools}}

Tool names:
{{tool_names}}

---

### IMPORTANT EXECUTION RULES
- Never output Thought / Action / Observation format.
- The system will handle tool execution automatically.
- When you decide to use a tool, directly call it.
- Do not explain tool execution steps.

---

### CORE RULES
{example_block}

2. Don't start with '''
3. Don't end with '''
4. Don't read implementation of method under test
5. Never enclose file paths or code inside quotes
6. Do not hallucinate behaviors not in the method description

---

### INPUT
Question:
{{input}}

{{agent_scratchpad}}
"""
    
    return PromptTemplate.from_template(template)