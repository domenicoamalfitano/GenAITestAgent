from tdd_agent.config import PROMPT_TEST, MAIN_JAVA_DIR, WORKFLOW_LOG, PROMPT_SOURCE, PROMPT_REFACTOR, TEST_JAVA_DIR, JAVA_PROJECT_DIR, TIMEOUT_MVN
from tdd_agent.core.exceptions import AgentInvokeError
from tdd_agent.core.graph.state import TDDState
from tdd_agent.core.graph.agent_runner import generate_tests_or_source_for_method
from pathlib import Path
import subprocess, os, sys


def red_node(state: TDDState) -> TDDState:
    """RED"""
    class_name = state["class_name"]
    test_file = str(TEST_JAVA_DIR / f"{class_name}Test.java").replace("\\", "/")

    print("RED PHASE...")
    with open(WORKFLOW_LOG, "a", encoding="utf-8") as f:
        f.write(f"\n=== RED phase — attempt {state['attempt_red'] + 1} ===\n")

    try:
        result = generate_tests_or_source_for_method(
            state["method_signature"],
            state["method_description"],
            class_name,
            test_file,
            PROMPT_TEST,
            state["agent_executor_test"],
        )
    except AgentInvokeError as e:
        print(f"Error in RED phase: {e}")
        result = ""

    return {
        **state,
        "result_test": result,
        "attempt_red": state["attempt_red"] + 1,
        "attempt_green": 0,
        "result_source": "",
        "attempt_refactor": 0,
        "result_refactor": "",
    }


def green_node(state: TDDState) -> TDDState:
    """GREEN"""
    class_name = state["class_name"]
    source_file = str(MAIN_JAVA_DIR / f"{class_name}.java").replace("\\", "/")

    print("GREEN PHASE...")
    with open(WORKFLOW_LOG, "a", encoding="utf-8") as f:
        f.write(f"\n=== GREEN phase — attempt {state['attempt_green'] + 1} ===\n")

    try:
        result = generate_tests_or_source_for_method(
            state["method_signature"],
            state["method_description"],
            class_name,
            source_file,
            PROMPT_SOURCE,
            state["agent_executor_source"],
            state["files_path_source"],
        )
    except AgentInvokeError as e:
        print(f"Error in GREEN phase: {e}")
        result = ""

    return {
        **state,
        "result_source": result,
        "attempt_green": state["attempt_green"] + 1,
    }


def refactor_node(state: TDDState) -> TDDState:
    """REFACTOR"""
    class_name = state["class_name"]
    source_file = str(MAIN_JAVA_DIR / f"{class_name}.java").replace("\\", "/")

    print("REFACTOR PHASE...")
    with open(WORKFLOW_LOG, "a", encoding="utf-8") as f:
        f.write(f"\n=== REFACTOR phase — attempt {state['attempt_refactor'] + 1} ===\n")

    try:
        result = generate_tests_or_source_for_method(
            state["method_signature"],
            state["method_description"],
            class_name,
            source_file,
            PROMPT_REFACTOR,
            state["agent_executor_refactor"],
            state["files_path_source"],
        )
    except AgentInvokeError as e:
        print(f"Error in REFACTOR phase: {e}")
        result = ""

    return {
        **state,
        "result_refactor": result,
        "attempt_refactor": state["attempt_refactor"] + 1,
    }











def write_file_truncate(state: TDDState) -> str:
    """Save code to a file. Format: '{\"file_path\": \"file_path\", \"content\": \"code_content\"}'"""
    try:
        file_path = state["pending_file_path"]
        content = state["pending_file_content"]
        
        
        path = Path(file_path).resolve()
        
        # constraint: must be under MAIN_JAVA_DIR or TEST_JAVA_DIR
        allowed_dirs = [MAIN_JAVA_DIR.resolve(), TEST_JAVA_DIR.resolve()]
        if not any(str(path).startswith(str(d)) for d in allowed_dirs):
            result = f"Error: file path not allowed {path}"
            return {**state, "write_file_result": result}
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # If the file exists, read its content and append only the new test methods
        with path.open("w", encoding='utf-8') as f:
            f.write(content.strip())

        result = f"Code saved successfully to {path}"
    except Exception as e:
        result = f"Error saving the file: {str(e)}"

    return {**state, "write_file_result": result}



def run_maven_test(state: TDDState) -> str:
    """Run JUnit tests in a Maven project and return a summary."""
    try:
        mvn_exe = r"C:\apache-maven-3.9.11\bin\mvn.cmd"
        command = [mvn_exe, "clean", "test", "-DfailIfNoTests=false"]
        if sys.platform == "win32":
            process = subprocess.Popen(
                command,
                cwd=JAVA_PROJECT_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True
            )
        else:
            process = subprocess.Popen(
                command,
                cwd=JAVA_PROJECT_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                preexec_fn=os.setsid
            )
        try:
            stdout, stderr = process.communicate(timeout=TIMEOUT_MVN)
        except subprocess.TimeoutExpired:
            if sys.platform == "win32":
                subprocess.run(f"taskkill /PID {process.pid} /T /F", shell=True)
            else:
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)
            result = "Error: The Maven command timed out after 120 seconds."
            return {**state, "exec_result": result}
        
        MAX_OUTPUT = 5000
        if len(stdout) > MAX_OUTPUT:
            stdout = stdout[:MAX_OUTPUT] + "\n...truncated stdout output...\n"
        if len(stderr) > MAX_OUTPUT:
            stderr = stderr[:MAX_OUTPUT] + "\n...truncated stderr output...\n"
        output = stdout + stderr
        # build the test summary
        # EXAMPLE:
        #   ===RUN_RESULT:BUILD_SUCCESS===
        #   Exit code: 0
        #   Tests run: 3, Failures: 0, Errors: 0, Skipped: 0
        #   Output completo:
        #   [full maven output]
        
        summary_line = "Tests run:"
        test_summary = ""
        for line in output.splitlines():
            if summary_line in line:
                test_summary = line.strip()
                break
        if not test_summary:
            test_summary = "No test summary found in Maven output."
        if "BUILD SUCCESS" in output:
            finals_status = "===RUN_RESULT:BUILD_SUCCESS==="
        else:
            finals_status = "===RUN_RESULT:BUILD_FAIL==="
        result = f"{finals_status}\nExit code: {process.returncode}\n{test_summary}\n\nFull output:\n{output}"
        return {**state, "exec_result": result}
        # summary = extract_test_summary(output)
        # status = "BUILD_SUCCESS" if "BUILD SUCCESS" in output else "BUILD_FAIL"

        # result = {
        #     "status": status,
        #     "exit_code": process.returncode,
        #     **summary,
        #     "raw_output": output
        # }

        # return json.dumps(result, indent=2)
        
        

    except subprocess.TimeoutExpired:
        result = "Error: The Maven command timed out after 120 seconds."
    except FileNotFoundError:
        result = "Error: Maven is not installed or not in the PATH."
    except Exception as e:
        result = f"Error running Maven: {str(e)}"
    
    return {**state, "exec_result": result}














