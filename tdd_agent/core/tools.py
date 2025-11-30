import subprocess
from pathlib import Path
from tdd_agent.config import SEPARATOR, MAIN_JAVA_DIR, TEST_JAVA_DIR, JAVA_PROJECT_DIR


# read the content of a file
def read_file(input_str: str) -> str:
    try:
        input_str = "".join(input_str.split())
        with open(input_str, "r", encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Errore nel leggere il file: {str(e)}"

# write code to a file, truncating existing content
def write_file_truncate(input_str: str) -> str:
    try:
        # the input format must be 'file_path|||code'
        if SEPARATOR not in input_str:
            return f"Errore: il formato non è corretto, non è stato trovato il separatore '{SEPARATOR}'."
        # split and clean up file_path and code
        file_path, code = input_str.split(SEPARATOR, 1)
        path = Path(file_path.strip().strip("'").strip('"')).resolve()
        code = code.strip().rstrip("'").rstrip('"').replace("```","").replace("<complete code here>","").strip()

        # constraint: must be under MAIN_JAVA_DIR or TEST_JAVA_DIR
        allowed_dirs = [MAIN_JAVA_DIR.resolve(), TEST_JAVA_DIR.resolve()]
        if not any(str(path).startswith(str(d)) for d in allowed_dirs):
            return f"Errore: il percorso del file non è consentito {path}"

        path.parent.mkdir(parents=True, exist_ok=True)
        
        # If the file exists, read its content and append only the new test methods
        with path.open("w", encoding='utf-8') as f:
            f.write(code.strip())

        return f"Codice salvato correttamente in {path}"
    except Exception as e:
        return f"Errore nel salvare il file: {str(e)}"

# run the tests using maven and return the summary
def run_maven_test(input_str: str = "") -> str:
    try:
        mvn_exe = r"C:\apache-maven-3.9.11\bin\mvn.cmd"
        command = [mvn_exe, "test", "-DfailIfNoTests=false"]
        result = subprocess.run(
            command,
            cwd=JAVA_PROJECT_DIR,
            capture_output=True,
            text=True,
            timeout=120
        )
        output = result.stdout + result.stderr
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
            test_summary = "Nessun riepilogo dei test trovato nell'output di Maven."
        if "BUILD SUCCESS" in output:
            finals_status = "===RUN_RESULT:BUILD_SUCCESS==="
        else:
            finals_status = "===RUN_RESULT:BUILD_FAIL==="
        return f"{finals_status}\nExit code: {result.returncode}\n{test_summary}\n\nOutput completo:\n{output}"

    except subprocess.TimeoutExpired:
        return "Errore: Il comando Maven ha superato il timeout di 120 secondi."
    except FileNotFoundError:
        return "Errore: Maven non è installato o non è nel PATH."
    except Exception as e:
        return f"Errore durante l'esecuzione di Maven: {str(e)}"
