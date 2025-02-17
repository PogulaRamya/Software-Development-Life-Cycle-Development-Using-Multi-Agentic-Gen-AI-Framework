import openai
from typing import Dict, List, Tuple

State = Dict[str, List[Tuple[str, str]]]
def review_chain(state: State) -> State:
    """
    Uses GPT-4 to review the generated code.
    """
    generated_code = next(msg[1] for msg in state["messages"] if msg[0] == "code")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a highly experienced Python code reviewer. Your task is to analyze the given code and provide detailed feedback. "
                    "The review should focus on the following aspects:\n"
                    "- **Code Structure**: Evaluate the overall organization and modularity of the code.\n"
                    "- **Readability**: Ensure the code is easy to read and understand, with proper use of comments and meaningful names for variables, functions, and classes.\n"
                    "- **Standards Compliance**: Verify that the code adheres to PEP 8 and other relevant Python standards.\n"
                    "- **Error Handling**: Check if the code has appropriate error handling and edge-case coverage.\n"
                    "- **Performance**: Identify potential inefficiencies and suggest optimizations where applicable.\n"
                    "- **Scalability**: Assess whether the code can handle increased load or complexity if needed.\n"
                    "- **Testability**: Evaluate how easily the code can be tested, and suggest improvements for test coverage.\n"
                    "- **Security**: Highlight any potential vulnerabilities or security issues in the code.\n"
                    "- **Best Practices**: Recommend improvements based on Python's best practices and industry standards.\n\n"
                    "Provide actionable suggestions for each identified issue and highlight any strengths in the code."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Review the following Python code and provide feedback based on the above criteria:\n\n{generated_code}\n\n"
                    "Ensure your feedback is detailed, constructive, and actionable."
                )
            }
        ]

    )
    code_review = response['choices'][0]['message']['content']
    state["messages"].append(("review", code_review))
    return state
