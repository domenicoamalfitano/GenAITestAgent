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

import re, subprocess, json, sys, json_repair
from pathlib import Path
from tdd_agent.config import MAIN_JAVA_DIR, TEST_JAVA_DIR, JAVA_PROJECT_DIR, TIMEOUT_MVN


# read the content of a file
def read_file(input_str: str) -> str:
    input_str = "".join(input_str.split())
    path = Path(input_str).resolve()
    allowed_dirs = [MAIN_JAVA_DIR.resolve(), TEST_JAVA_DIR.resolve()]
    if not any(str(path).startswith(str(d)) for d in allowed_dirs):
        return f"Error: file path not allowed {path}"
    try:
        with open(path, "r", encoding='utf-8') as f:
            content = f.read()
        
        return content
    except Exception as e:
        return f"Error reading the file: {str(e)}"

# write code to a file, truncating existing content
def write_file_truncate(input_str: str) -> str:
    try:
        input_str = input_str.replace("```json", "").replace("```", "").strip()
        
        match = re.search(r'\{.*\}', input_str, re.DOTALL)
        if not match:
            return "Error: no JSON object found"
        json_str = match.group(0)
        
        try:
            data = json_repair.loads(json_str)
            path = Path(data["file_path"]).resolve()
            code = data["content"]
        except json.JSONDecodeError as e:
            return f"Error decoding JSON: {str(e)}"
        
        # constraint: must be under MAIN_JAVA_DIR or TEST_JAVA_DIR
        allowed_dirs = [MAIN_JAVA_DIR.resolve(), TEST_JAVA_DIR.resolve()]
        if not any(str(path).startswith(str(d)) for d in allowed_dirs):
            return f"Error: file path not allowed {path}"

        path.parent.mkdir(parents=True, exist_ok=True)
        
        # If the file exists, read its content and append only the new test methods
        with path.open("w", encoding='utf-8') as f:
            f.write(code.strip())

        return f"Code saved successfully to {path}"
    except Exception as e:
        return f"Error saving the file: {str(e)}"

# run the tests using maven and return the summary
def run_maven_test(input_str: str = "") -> str:
    try:
        mvn_exe = r"C:\apache-maven-3.9.11\bin\mvn.cmd"
        command = [mvn_exe, "test", "-DfailIfNoTests=false"]
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

    except subprocess.TimeoutExpired:
        return "Error: The Maven command timed out after 120 seconds."
    except FileNotFoundError:
        return "Error: Maven is not installed or not in the PATH."
    except Exception as e:
        return f"Error running Maven: {str(e)}"