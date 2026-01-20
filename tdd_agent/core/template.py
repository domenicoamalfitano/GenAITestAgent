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

from langchain.prompts import PromptTemplate

# return the system message for test or source code generation
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
    Final Answer: the final answer with no extra text.


⚠️ IMPORTANT - STRICT RULES:
    {example_block}
        
    2. Don't start with '''
    3. Don't end with '''
    4. Don't read the implementation of the method under test
    5. Never enclose file paths or code inside quotes. Do not start or end Action Input with ' or ".



    Question: {{input}}
    {{agent_scratchpad}}
    """
    
    return PromptTemplate.from_template(template)