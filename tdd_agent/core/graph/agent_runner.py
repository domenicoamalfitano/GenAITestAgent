from tdd_agent.core.exceptions import AgentInvokeError

from langchain_core.runnables import Runnable
from tdd_agent.config import TEST_JAVA_DIR, MAIN_JAVA_DIR, WORKFLOW_LOG, PROMPT_TEST, PROMPT_SOURCE, PROMPT_COUNTERS
from langchain_core.callbacks import BaseCallbackHandler



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

class ToolLoggerCallback(BaseCallbackHandler):

    def on_tool_start(self, serialized, input_str, **kwargs):
        tool_name = serialized.get("name", "unknown_tool")
        print(f"\n🛠 TOOL START: {tool_name}")
        print(f"INPUT: {input_str}")

    def on_tool_end(self, output, **kwargs):
        print(f"🟢 TOOL OUTPUT: {output}")



# build the prompt for RED or GREEN/REFACTOR phase and invoke the agent executor
def generate_tests_or_source_for_method(method_signature: str, method_description: str, className: str, file_path: str, promptFile: str, agent_executor: Runnable, files_path_source: str = "") -> str:
    
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

        with open(WORKFLOW_LOG, "a", encoding="utf-8") as log_main:
            log_main.write(namePrompt)
            
        result = agent_executor.invoke({"messages":[{"role": "user", "content": prompt}]}, config={"callbacks":[ToolLoggerCallback()]})
        if isinstance(result, dict):
            if "output" in result:
                print(result["output"])
                return result["output"]
            if "result" in result:
                print(result["result"])
                return result["result"]
            if "messages" in result:
                print(result["messages"][-1].content)
                return result["messages"][-1].content

        if hasattr(result, "content"):
            print(result.content)
            return result.content

        raise AgentInvokeError(f"Invalid agent output type: {type(result)}")
    except Exception as e:
        error_message = f"Error during agent execution: {str(e)}"
        with open(WORKFLOW_LOG, "a", encoding="utf-8") as log_main:
            log_main.write(f"{namePrompt}\t\t {error_message}\n")
        raise AgentInvokeError(f"{error_message}")