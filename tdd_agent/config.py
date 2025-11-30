from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
JAVA_PROJECT_DIR = BASE_DIR.parent / "JavaProject"
MAIN_JAVA_DIR = JAVA_PROJECT_DIR / "src" / "main" / "java" / "com" / "example"
TEST_JAVA_DIR = JAVA_PROJECT_DIR / "src" / "test" / "java" / "com" / "example"
SIGNATURES_DIR = BASE_DIR / "signatures"
PROMPTS_DIR = BASE_DIR / "prompts"
PROMPT_TEST = PROMPTS_DIR / "PromptTest.txt"
PROMPT_SOURCE = PROMPTS_DIR / "PromptSource.txt"
PROMPT_REFACTOR = PROMPTS_DIR / "PromptRefactor.txt"
MAX_RETRIES = 6
GROQ_API_KEY = "GROQ_API_KEY"
MODEL_LLM = "moonshotai/kimi-k2-instruct"
TEMPERATURE = 0.0
MAX_ITERATIONS = 14
RESPONSE_TESTS_ENOUGH = "✅ enough tests"
RESPONSE_ALL_TESTS_PASSED = "✅ All tests passed successfully."
RESPONSE_REFACTORING_COMPLETE = "Refactoring complete"
SEPARATOR = "|||"