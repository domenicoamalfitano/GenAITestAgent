from core.exceptions import AgentInvokeError
from langchain.agents import AgentExecutor
import time
from config import TEST_JAVA_DIR, MAIN_JAVA_DIR, PROMPT_TEST, PROMPT_SOURCE, PROMPT_REFACTOR, RESPONSE_TESTS_ENOUGH, RESPONSE_ALL_TESTS_PASSED, RESPONSE_REFACTORING_COMPLETE, MAX_RETRIES

# generation of tests and source for a method, (TDD)
def process_method(method_signature, method_description, class_name, files_path_source, agent_executor_test, agent_executor_source, agent_executor_refactor):
    result_test = ""
    attempt = 0
    test_file = str(TEST_JAVA_DIR / f"{class_name}Test.java")
    source_file = str(MAIN_JAVA_DIR / f"{class_name}.java")
    print(f"Start TDD iteration for {method_signature}\n")
    
    while RESPONSE_TESTS_ENOUGH not in result_test and attempt < MAX_RETRIES:
        # generate a single test for the method
        
        print("RED PHASE...")
        # RED PHASE: generate a failed test
        result_test = generate_tests_or_source_for_method(method_signature, method_description, class_name, test_file, PROMPT_TEST, agent_executor_test)
        if RESPONSE_TESTS_ENOUGH in result_test:
            continue
        # GREEN PHASE: generate/update source code until all tests pass.
        attempt_source = 0
        result_source = ""
        while RESPONSE_ALL_TESTS_PASSED not in result_source and attempt_source < MAX_RETRIES:
            print(f"GREEN PHASE...")
            # GREEN phase: generate/fix source code
            result_source = generate_tests_or_source_for_method(method_signature, method_description, class_name, source_file, PROMPT_SOURCE, agent_executor_source, files_path_source)
            attempt_source += 1
            time.sleep(0.3)

        # REFACTOR PHASE: improve code structure
        attempt_refactor = 0
        result_refactor = ""
        while (RESPONSE_ALL_TESTS_PASSED not in result_refactor or RESPONSE_REFACTORING_COMPLETE not in result_refactor) and attempt_refactor < MAX_RETRIES:
            print(f"REFACTOR PHASE...")
            result_refactor = generate_tests_or_source_for_method(method_signature, method_description, class_name, source_file, PROMPT_REFACTOR, agent_executor_refactor, files_path_source)
            attempt_refactor += 1
            time.sleep(0.3)


        attempt += 1
        time.sleep(0.3)

# function to generate tests for a method or methods for source code
def generate_tests_or_source_for_method(method_signature: str, method_description: str, className: str, file_path: str, promptFile: str, agent_executor: AgentExecutor, files_path_source: str = "") -> str:

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

    try:
        result = agent_executor.invoke({"input": prompt})
        if not isinstance(result, dict) or "output" not in result:
            raise AgentInvokeError("Output non valido dell'agente")
        return result["output"]
    except Exception as e:
        raise AgentInvokeError(f"Errore durante l'esecuzione dell'agente: {str(e)}")

