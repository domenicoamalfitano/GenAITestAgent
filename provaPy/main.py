from core.tools import write_file_truncate, run_maven_test, read_file
from core.llm import load_llm, create_agent_executor
from core.exceptions import AgentInvokeError
from tdd.signatures import load_signature_files, read_signatures
from tdd.process import process_method
from langchain.agents import Tool
from core.template import return_template_for_test_or_code
from config import TEST_JAVA_DIR, MAIN_JAVA_DIR, MAX_ITERATIONS
from pathlib import Path

if __name__ == "__main__":
    TEST_JAVA_DIR.mkdir(parents=True, exist_ok=True)
    MAIN_JAVA_DIR.mkdir(parents=True, exist_ok=True)
    
    tools = [
        Tool(
            name="write_file_truncate",
            func=write_file_truncate,
            description="Salva codice in un file. Formato: 'percorso_file|||contenuto_codice'"
        ),
        Tool(
            name="run_maven_test",
            func=run_maven_test,
            description="Esegue i test JUnit in un progetto Maven e restituisce un riepilogo."
        ),
        Tool(
            name="read_file",
            func=read_file,
            description="Legge il contenuto di un file specificato."
        )
    ]
    tools_RED = tools[:2]

    prompt_test = return_template_for_test_or_code("test")
    prompt_source = return_template_for_test_or_code("source")
    print("✅ Prompt template creato")
    
    llm = load_llm()
    
    agent_executor_test = create_agent_executor(llm, tools_RED, prompt_test, MAX_ITERATIONS)
    agent_executor_source = create_agent_executor(llm, tools, prompt_source, MAX_ITERATIONS)
    agent_executor_refactor = create_agent_executor(llm, tools, prompt_source, MAX_ITERATIONS)

    print("🚀 Avvio generazione test automatica...")
    # read all signature files
    signature_files, files_path_source = load_signature_files()              
    
    for sig_file in signature_files:

        methods = read_signatures(sig_file)
        class_name = Path(sig_file).stem
        # open signature file and read method signatures with optional description
        
        for method_signature, method_description in methods:
            try:
                process_method(method_signature, method_description, class_name, files_path_source, agent_executor_test, agent_executor_source, agent_executor_refactor)
            except AgentInvokeError as e:
                print(e)
            
    print("✅ TDD completed.")