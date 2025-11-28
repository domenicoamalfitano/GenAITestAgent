
from langchain.prompts import PromptTemplate

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