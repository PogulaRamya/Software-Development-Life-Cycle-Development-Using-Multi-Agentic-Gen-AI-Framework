import openai
from typing import Dict, List, Tuple

State = Dict[str, List[Tuple[str, str]]]

def deploy_chain(state: State) -> State:
    """
    Uses GPT-4 to create deployment scripts for the project.
    """
    generated_code = next(msg[1] for msg in state["messages"] if msg[0] == "code")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a highly experienced DevOps engineer and deployment script generator. "
                    "Your task is to create a deployment script that adheres to the following guidelines:\n"
                    "- Ensure the script is written in Bash (or another specified language) and follows best practices for security and maintainability.\n"
                    "- Include descriptive comments explaining each step of the deployment process.\n"
                    "- Validate all required dependencies, tools, and configurations before proceeding with deployment.\n"
                    "- Implement error handling to ensure graceful failure and clear error messages.\n"
                    "- Support deployment in multiple environments (e.g., development, staging, production) with environment-specific configurations.\n"
                    "- Avoid hardcoding sensitive information such as passwords or API keys; use environment variables instead.\n"
                    "- Ensure idempotence: running the script multiple times should not cause unintended changes.\n"
                    "- Provide a cleanup mechanism to undo the deployment if necessary.\n"
                    "- Add usage instructions and examples at the top of the script to guide users.\n"
                    "- Optimize for performance and reusability wherever possible."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Create a deployment script for the following code:\n\n{generated_code}\n\n"
                    "Ensure the script follows the above guidelines and is ready for production use."
                )
            }
        ]
    )
    deployment_script = response['choices'][0]['message']['content']
    state["messages"].append(("deployment", deployment_script))
    return state
