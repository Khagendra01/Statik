from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
import subprocess
import re
from typing import TypedDict, Optional

# Define the state
class State(TypedDict):
    question: str
    code: Optional[str]
    output: Optional[str]
    feedback: Optional[str]
    attempts: int

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4", api_key='sk-proj--')

# Helper function to extract code from markdown
def extract_code(text: str) -> str:
    pattern = r'```python\n(.*?)\n```'
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else text.strip()

# Define nodes
def generate_code(state: State) -> dict:
    question = state["question"]
    feedback = state.get("feedback", "")
    previous_code = state.get("code", "No previous code")
    previous_output = state.get("output", "No previous output")
    
    prompt = f"""
    **Math Problem**: {question}

    **Previous Attempt**:
    ```python
    {previous_code}
    ```
    **Output**: {previous_output}
    **Feedback**: {feedback if feedback else "No feedback yet"}

    Write corrected Python code to solve the problem.
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    new_code = extract_code(response.content)
    return {"code": new_code, "attempts": state["attempts"] + 1}

def execute_code(state: State) -> dict:
    code = state.get("code", "")
    try:
        result = subprocess.run(
            ["python", "-c", code],
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout.strip() or result.stderr.strip()
    except Exception as e:
        output = str(e)
    return {"output": output}

def evaluate_output(state: State) -> dict:
    question = state["question"]
    output = state.get("output", "")
    
    prompt = f"""
    **Problem**: {question}
    **Proposed Solution**: {output}

    Is this solution mathematically correct? Respond ONLY with 'yes' or 'no'.
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    decision = response.content.strip().lower()
    
    feedback = ""
    if decision != 'yes':
        feedback = "The solution was incorrect. Please analyze the problem and try again."
    
    return {"evaluation": decision, "feedback": feedback}

# Build the workflow
workflow = StateGraph(State)

workflow.add_node("generate_code", generate_code)
workflow.add_node("execute_code", execute_code)
workflow.add_node("evaluate_output", evaluate_output)

workflow.set_entry_point("generate_code")

workflow.add_edge("generate_code", "execute_code")
workflow.add_edge("execute_code", "evaluate_output")

def decide_next_step(state: State) -> str:
    if state.get("evaluation") == 'yes' or state.get("attempts", 0) >= 3:
        return END
    return "generate_code"

workflow.add_conditional_edges(
    "evaluate_output",
    decide_next_step,
    {"generate_code": "generate_code", END: END}
)

app = workflow.compile()

def askIT(question):
    result = app.invoke({"question": question, "attempts": 0})
    print("\nFinal Result:")
    print(f"Question: {result['question']}")
    print(f"Final Code:\n{result['code']}")
    print(f"Final Output: {result['output']}")
    print(f"Attempts: {result['attempts']}")
    return result['output']