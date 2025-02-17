import openai
from typing import Dict, List, Tuple

State = Dict[str, List[Tuple[str, str]]]
openai.api_key = ""

def test_chain(state: State) -> State:
    """
    Uses GPT-4 to generate test cases for the code.
    """
    generated_code = next(msg[1] for msg in state["messages"] if msg[0] == "code")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a highly skilled Python test case generator. Your task is to create comprehensive unit tests "
                    "for the given Python code. Ensure the unit tests adhere to the following guidelines:\n"
                    "- Use Python's built-in `unittest` framework.\n"
                    "- Test all public functions and methods, covering normal cases, edge cases, and error conditions.\n"
                    "- Include descriptive test case names that indicate the scenario being tested.\n"
                    "- Add inline comments to explain the purpose of each test case.\n"
                    "- Use assertions to validate the expected behavior of the code.\n"
                    "- Ensure the tests are modular and easy to extend for additional scenarios.\n"
                    "- Avoid hardcoding test data; use parameterized tests where applicable.\n"
                    "- If the code interacts with external systems (e.g., APIs, databases), mock these dependencies.\n"
                    "- Include a `main` block to allow running the tests directly from the script.\n"
                    "- Provide examples or instructions for running the tests if applicable.\n"
                    "- Ensure the tests follow best practices for maintainability and readability."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Generate detailed and comprehensive unit tests for the following Python code:\n\n{generated_code}\n\n"
                    "Ensure the tests cover all scenarios and follow the above guidelines."
                )
            }
        ]
    )
    test_code = response['choices'][0]['message']['content']
    state["messages"].append(("testing", test_code))
    return state
