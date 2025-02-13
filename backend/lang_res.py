from typing import Dict, TypedDict, Annotated, List
from langgraph.graph import Graph
from langgraph.prebuilt.messages import Message
import operator
import json

# Define the state schema
class State(TypedDict):
    question: str
    code: str
    result: str
    messages: List[Message]

# Function to generate Python code using LLM
def generate_code(state: State) -> State:
    """Generate Python code to solve the math question using LLM."""
    # Here you would integrate with your LLM of choice
    # For example with Claude:
    # response = client.messages.create(
    #     model="claude-3-opus-20240229",
    #     messages=[{
    #         "role": "user",
    #         "content": f"Write Python code to solve this math problem: {state['question']}. Only return the code, no explanations."
    #     }]
    # )
    # state["code"] = response.content
    
    # For demonstration, let's simulate an LLM response
    if "sum of numbers" in state["question"].lower():
        state["code"] = """
numbers = [1, 2, 3, 4, 5]
result = sum(numbers)
print(f"The sum is: {result}")
"""
    return state

# Function to execute the generated Python code
def execute_code(state: State) -> State:
    """Execute the generated Python code and capture the output."""
    try:
        # Create a string buffer to capture print output
        from io import StringIO
        import sys
        
        # Redirect stdout to capture print statements
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        
        # Execute the code
        exec(state["code"])
        
        # Get the output and restore stdout
        state["result"] = mystdout.getvalue()
        sys.stdout = old_stdout
        
    except Exception as e:
        state["result"] = f"Error executing code: {str(e)}"
    
    return state

# Function to format the final response
def format_response(state: State) -> State:
    """Format the final response with the question, code, and result."""
    response = f"""
Question: {state['question']}

Generated Python Code:
```python
{state['code']}
```

Execution Result:
{state['result']}
"""
    state["messages"].append(Message(content=response, role="assistant"))
    return state

# Create the graph
def create_math_solver_graph() -> Graph:
    """Create the Langgraph workflow for solving math problems."""
    # Create workflow
    workflow = Graph()
    
    # Add nodes
    workflow.add_node("generate_code", generate_code)
    workflow.add_node("execute_code", execute_code)
    workflow.add_node("format_response", format_response)
    
    # Define the edges
    workflow.add_edge("generate_code", "execute_code")
    workflow.add_edge("execute_code", "format_response")
    
    # Set the entry and exit points
    workflow.set_entry_point("generate_code")
    workflow.set_exit_point("format_response")
    
    return workflow

def solve_math_problem(question: str):
    """Solve a math problem using the Langgraph workflow."""
    # Initialize the graph
    graph = create_math_solver_graph()
    
    # Create initial state
    initial_state = State(
        question=question,
        code="",
        result="",
        messages=[]
    )
    
    # Run the graph
    final_state = graph.run(initial_state)
    
    # Return the messages
    return final_state["messages"]

# Example usage
if __name__ == "__main__":
    question = "Calculate the sum of numbers from 1 to 5"
    result = solve_math_problem(question)
    print(result[0].content)