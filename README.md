# GenAITestAgent
This framework provides an agent-based AI architecture designed to automate the Test Driven Development (TDD) workflow for java projects.
the workflow is composed of the three phases of TDD, (RED, GREEN, REFACTOR), each phase has a specific prompt used as input for the LLM's model (prompts Directory).

# Installation
```
    python -m venv env

    source env/bin/activate //for macOS and Linux
    env\Scripts\activate // for Windows

    pip install -r requirements.txt
```

# Setup
    You must set the environment variable "GROQ_API_KEY"
    Create a API key from Groq (https://groq.com/)
    Create a file '.env' in the project's root containing an API key from Groq (\GenAITestAgent\.env)

    ```
    GROQ_API_KEY=<our_key>
    ```

    You could create files .txt in the signatures directory to specify the methods to create with a description, correct format:
    Example:
    
    ```
    # the method must calculate the area of a square.
    # the side of the square is "side"
    # ...
    double squareArea(double side)
    ```

# Execution
```
python main.py
```