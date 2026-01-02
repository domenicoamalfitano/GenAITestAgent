from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()

# Logs directory
LOGS_DIR = BASE_DIR / "logs"
WORKFLOW_LOG = LOGS_DIR / "workflow.log"

# Java project directories
JAVA_PROJECT_DIR = BASE_DIR.parent / "JavaProject"
MAIN_JAVA_DIR = JAVA_PROJECT_DIR / "src" / "main" / "java" / "com" / "example"
TEST_JAVA_DIR = JAVA_PROJECT_DIR / "src" / "test" / "java" / "com" / "example"
# signatures directory
SIGNATURES_DIR = BASE_DIR / "signatures"
# prompts directory
PROMPTS_DIR = BASE_DIR / "prompts"
PROMPT_TEST = PROMPTS_DIR / "PromptTest.txt"
PROMPT_SOURCE = PROMPTS_DIR / "PromptSource.txt"
PROMPT_REFACTOR = PROMPTS_DIR / "PromptRefactor.txt"

MAX_RETRIES = 6
GROQ_API_KEY = "GROQ_API_KEY"
MODEL_LLM = "moonshotai/kimi-k2-instruct" # LLM model to use
TEMPERATURE = 0.0
MAX_ITERATIONS = 14
# Responses from the agent
RESPONSE_TESTS_ENOUGH = "✅ enough tests"
RESPONSE_ALL_TESTS_PASSED = "✅ All tests passed successfully."
RESPONSE_REFACTORING_COMPLETE = "Refactoring complete"
TIMEOUT_MVN = 60 # seconds, limit time for tests execution.
PROMPT_COUNTERS = {
    "RED": 0,
    "GREEN": 0,
    "REFACTOR": 0
}