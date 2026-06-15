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

import re, subprocess, json, sys
from pathlib import Path
from tdd_agent.config import MAIN_JAVA_DIR, TEST_JAVA_DIR, JAVA_PROJECT_DIR, TIMEOUT_MVN
from langchain.tools import tool


def extract_test_summary(output: str):
    tests_run = failures = errors = skipped = None

    for line in output.splitlines():
        if "Tests run:" in line:
            match = re.search(
                r"Tests run: (\d+), Failures: (\d+), Errors: (\d+), Skipped: (\d+)",
                line
            )
            if match:
                tests_run = int(match.group(1))
                failures = int(match.group(2))
                errors = int(match.group(3))
                skipped = int(match.group(4))
                break

    return {
        "tests_run": tests_run,
        "failures": failures,
        "errors": errors,
        "skipped": skipped
    }



def list_directory(dir_path: str) -> str:
    """List files and folders inside a directory."""

    path = Path(dir_path).resolve()

    if not path.exists():
        return json.dumps({"error": "directory does not exist"})

    if not path.is_dir():
        return json.dumps({"error": "path is not a directory"})

    items = [
        {
            "name": p.name,
            "type": "dir" if p.is_dir() else "file"
        }
        for p in path.iterdir()
    ]

    return json.dumps({
        "path": str(path),
        "items": items
    }, indent=2)


# read the content of a file
@tool
def read_file(file_path: str) -> str:
    """Read the content of a specified file."""
    
    # file_path = "".join(file_path.split())
    path = Path(file_path.strip()).resolve()
    print("TOOL EXECUTED -> read_file:", path)
    allowed_dirs = [MAIN_JAVA_DIR.resolve(), TEST_JAVA_DIR.resolve()]
    if not any(str(path).startswith(str(d)) for d in allowed_dirs):
        return f"Error: file path not allowed {path}"
    try:
        if path.is_dir():
            return list_directory(path)
        # with open(path, "r", encoding='utf-8') as f:
        #     content = f.read()
        return path.read_text(encoding="utf-8")
        # return content
    except Exception as e:
        return f"Error reading the file: {str(e)}"

# write code to a file, truncating existing content
@tool
def write_file_truncate(file_path: str, content: str) -> str:
    """Save code to a file. Format: '{\"file_path\": \"file_path\", \"content\": \"code_content\"}'"""
    try:
        # file_path = file_path.replace("```json", "").replace("```", "").strip()
        
        # match = re.search(r'\{.*\}', file_path, re.DOTALL)
        # if not match:
        #     return "Error: no JSON object found"
        # json_str = match.group(0)
        
        # try:
            # data = json_repair.loads(json_str)
            # path = Path(data["file_path"]).resolve()
            # code = data["content"]
        # except json.JSONDecodeError as e:
            # return f"Error decoding JSON: {str(e)}"
        
        path = Path(file_path).resolve()
        
        # constraint: must be under MAIN_JAVA_DIR or TEST_JAVA_DIR
        allowed_dirs = [MAIN_JAVA_DIR.resolve(), TEST_JAVA_DIR.resolve()]
        if not any(str(path).startswith(str(d)) for d in allowed_dirs):
            return f"Error: file path not allowed {path}"

        path.parent.mkdir(parents=True, exist_ok=True)
        
        # If the file exists, read its content and append only the new test methods
        with path.open("w", encoding='utf-8') as f:
            f.write(content.strip())

        return f"Code saved successfully to {path}"
    except Exception as e:
        return f"Error saving the file: {str(e)}"

# run the tests using maven and return the summary
@tool
def run_maven_test(input_str: str = "") -> str:
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
            
            return "Error: The Maven command timed out after 120 seconds."
        
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
        return f"{finals_status}\nExit code: {process.returncode}\n{test_summary}\n\nFull output:\n{output}"
        
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
        return "Error: The Maven command timed out after 120 seconds."
    except FileNotFoundError:
        return "Error: Maven is not installed or not in the PATH."
    except Exception as e:
        return f"Error running Maven: {str(e)}"
    
