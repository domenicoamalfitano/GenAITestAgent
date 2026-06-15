from typing import TypedDict


class TDDState(TypedDict):
    method_signature: str
    method_description: str
    class_name: str
    files_path_source: str

    result_test: str
    result_source: str
    result_refactor: str

    attempt_red: int
    attempt_green: int
    attempt_refactor: int

    agent_executor_test: object
    agent_executor_source: object
    agent_executor_refactor: object
    
    
    pending_file_path: str
    pending_file_content: str
    
    write_file_result: str
    
    exec_result: str