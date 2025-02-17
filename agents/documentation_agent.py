import openai
from typing import Dict, List, Tuple

State = Dict[str, List[Tuple[str, str]]]

def doc_chain(state: State) -> State:
    """
    Uses GPT-4 to generate documentation for the code.
    """
    generated_code = next(msg[1] for msg in state["messages"] if msg[0] == "code")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a highly skilled technical writer specializing in Python projects. "
                    "Your task is to write comprehensive and professional documentation for the given Python code. "
                    "The documentation should adhere to the following guidelines:\n"
                    "- Provide a concise and clear overview of the code's purpose and functionality.\n"
                    "- Include a detailed description of each class, function, and method, specifying:\n"
                    "  - Its purpose.\n"
                    "  - Input parameters (with types and descriptions).\n"
                    "  - Return values (with types and descriptions).\n"
                    "  - Any exceptions raised.\n"
                    "- Use industry-standard formatting, such as reStructuredText (reST) or Markdown.\n"
                    "- Highlight key algorithms or logic within the code and explain them in simple terms.\n"
                    "- If applicable, include usage examples and sample outputs for better understanding.\n"
                    "- Document any dependencies, configuration requirements, or setup instructions.\n"
                    "- Ensure the documentation is accessible to both technical and non-technical readers.\n"
                    "- Include a 'Getting Started' section if the code is part of a larger application or system."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Write detailed and professional documentation for the following Python code:\n\n{generated_code}\n\n"
                    "Ensure the documentation follows the above guidelines and is suitable for developers and stakeholders."
                )
            }
        ]

    )
    documentation = response['choices'][0]['message']['content']
    state["messages"].append(("documentation", documentation))
    return state
