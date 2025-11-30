from tdd_agent.config import TEST_JAVA_DIR, MAIN_JAVA_DIR, MAX_ITERATIONS
from tdd_agent.core.tools import write_file_truncate, run_maven_test, read_file
from tdd_agent.core.llm import load_llm, create_agent_executor
from tdd_agent.core.exceptions import AgentInvokeError
from tdd_agent.tdd.signatures import load_signature_files, read_signatures
from tdd_agent.tdd.process import process_method
from langchain.agents import Tool
from tdd_agent.core.template import return_template_for_test_or_code
from pathlib import Path
from dotenv import load_dotenv

load_dotenv('.env')

if __name__ == "__main__":
    TEST_JAVA_DIR.mkdir(parents=True, exist_ok=True)
    MAIN_JAVA_DIR.mkdir(parents=True, exist_ok=True)
    
    # define the tools
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
    tools_RED = tools[:2] # remove read_file tool for RED phase

    # create prompt templates for test and source code generation
    prompt_test = return_template_for_test_or_code("test")
    prompt_source = return_template_for_test_or_code("source")
    print("✅ Prompt template creato")
    
    # load LLM and create agent executors
    llm = load_llm()
    
    # create agent executors for RED, GREEN, and REFACTOR phases
    agent_executor_test = create_agent_executor(llm, tools_RED, prompt_test, MAX_ITERATIONS)
    agent_executor_source = create_agent_executor(llm, tools, prompt_source, MAX_ITERATIONS)
    agent_executor_refactor = create_agent_executor(llm, tools, prompt_source, MAX_ITERATIONS)

    # read all signature files
    signature_files, files_path_source = load_signature_files()              
    if not signature_files:
        print("❌ No signature files found. Exiting.")
        exit(1)
        
    print("🚀 Avvio Test Driven Development...")
    for sig_file in signature_files:
        
        # read method signatures from the signature file
        methods = read_signatures(sig_file)
        class_name = Path(sig_file).stem
        
        # process each method through the TDD phases
        for method_signature, method_description in methods:
            try:
                process_method(method_signature, method_description, class_name, files_path_source, agent_executor_test, agent_executor_source, agent_executor_refactor)
            except AgentInvokeError as e:
                print(e)
            
    print("✅ TDD completed.")