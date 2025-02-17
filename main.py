import os
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from agents.coding_agent import code_chain
from agents.review_agent import review_chain
from agents.testing_agent import test_chain
from agents.documentation_agent import doc_chain
from agents.deployment_agent import deploy_chain
import gradio as gr
import time

# Define the State schema
class State(TypedDict):
    messages: list[tuple[str, str]]

# Create StateGraph
graph = StateGraph(State)

# Add nodes
graph.add_node("coding", code_chain)
graph.add_node("review", review_chain)
graph.add_node("testing", test_chain)
graph.add_node("documentation", doc_chain)
graph.add_node("deployment", deploy_chain)

# Define edges
graph.add_edge(START, "coding")
graph.add_edge("coding", "review")
graph.add_edge("review", "testing")
graph.add_edge("testing", "documentation")
graph.add_edge("documentation", "deployment")
graph.add_edge("deployment", END)

# Compile the graph
compiled_graph = graph.compile()

# Directory structure for saving files
OUTPUT_DIR = "output"
CODE_FILE = os.path.join(OUTPUT_DIR, "generated_code.py")
TEST_FILE = os.path.join(OUTPUT_DIR, "test_cases.py")
DOC_FILE = os.path.join(OUTPUT_DIR, "documentation.md")
DEPLOY_SCRIPT_FILE = os.path.join(OUTPUT_DIR, "deployment_script.sh")

# Function to save generated content
def save_generated_content(content_dict):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    with open(CODE_FILE, "w") as f:
        f.write(content_dict.get("coding", ""))
    with open(TEST_FILE, "w") as f:
        f.write(content_dict.get("testing", ""))
    with open(DOC_FILE, "w") as f:
        f.write(content_dict.get("documentation", ""))
    with open(DEPLOY_SCRIPT_FILE, "w") as f:
        f.write(content_dict.get("deployment", ""))

# Gradio Real-Time Workflow Function
def sdlc_workflow_live(requirements: str):
    initial_state = {"messages": [("user", requirements)]}
    progress = []
    content_dict = {}

    progress.append("Starting SDLC Workflow: Initializing...")
    yield "\n".join(progress), content_dict, gr.update(visible=False), gr.update(visible=False)

    for node_name in ["coding", "review", "testing", "documentation", "deployment"]:
        progress.append(f"Working on {node_name.capitalize()}...")
        yield "\n".join(progress), content_dict, gr.update(visible=False), gr.update(visible=False)
        time.sleep(2)

        final_state = compiled_graph.invoke(initial_state)
        task_output = next((msg[1] for msg in final_state["messages"] if msg[0] == node_name), "No Output")
        content_dict[node_name] = task_output
        progress.append(f"Completed {node_name.capitalize()}:\n{task_output}")
        yield "\n".join(progress), content_dict, gr.update(visible=False), gr.update(visible=False)

    progress.append("Workflow Complete! Do you want to save the generated content locally?")
    yield "\n".join(progress), content_dict, gr.update(visible=True), gr.update(visible=True)

# Gradio Interface
def build_interface():
    with gr.Blocks() as demo:
        gr.Markdown("## Enhanced SDLC Workflow Automation")
        requirements_input = gr.Textbox(
            label="Requirements", placeholder="Enter your requirements here..."
        )
        progress_output = gr.Markdown(label="Progress Updates")
        yes_button = gr.Button("Yes", visible=False)
        no_button = gr.Button("No", visible=False)

        content_state = gr.State({})  # Initialize content_dict state

        def workflow_wrapper(requirements):
            for progress, content_dict, yes_visibility, no_visibility in sdlc_workflow_live(requirements):
                yield progress, content_dict, yes_visibility, no_visibility

        def save_content(content_dict):
            if content_dict:  # Ensure content_dict is valid
                save_generated_content(content_dict)
                return "Generated content saved successfully!"
            return "No content to save."

        def discard_content():
            return "Generated content was not saved."

        # Link the buttons to actions
        requirements_input.submit(
            workflow_wrapper,
            inputs=requirements_input,
            outputs=[progress_output, content_state, yes_button, no_button],
        )
        yes_button.click(
            save_content, inputs=content_state, outputs=progress_output
        )
        no_button.click(
            discard_content, inputs=None, outputs=progress_output
        )

    return demo


if __name__ == "__main__":
    interface = build_interface()
    interface.launch()
