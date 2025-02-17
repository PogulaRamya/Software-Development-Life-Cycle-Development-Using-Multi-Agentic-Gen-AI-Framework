import openai
from typing import Dict, List, Tuple

State = Dict[str, List[Tuple[str, str]]]
openai.api_key = ""
def code_chain(state: State) -> State:
    """
    Uses GPT-4 to generate code based on requirements.
    """
    requirements = next(msg[1] for msg in state["messages"] if msg[0] == "user")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages = [
            {"role": "system", "content": (
                "You are a highly skilled software developer with expertise in Python. "
                "Your task is to generate high-quality, production-ready Python code that meets the following requirements:\n"
                "- Ensure the code is modular, follows PEP 8 standards, and is easy to maintain.\n"
                "- Include type annotations for all function signatures.\n"
                "- Provide comprehensive inline comments to explain the code logic.\n"
                "- Add a docstring for each function and class that describes its purpose, inputs, outputs, and any exceptions raised.\n"
                "- Use best practices for error handling and validation.\n"
                "- Optimize the code for performance and scalability when applicable.\n"
                "- Write code that can be easily extended or integrated into larger systems.\n"
                "- Avoid unnecessary dependencies unless explicitly stated in the requirement.\n"
                "If applicable, include an example usage section at the end of the script.\n"
            )},
            {"role": "user", "content": (
                f"Generate Python code for the following requirement:\n\n{requirements}\n\n"
                "Ensure the generated code follows the above instructions strictly."
            )}
        ]

    )
    generated_code = response['choices'][0]['message']['content']
    print(generated_code)
    state["messages"].append(("code", generated_code))
    return state
