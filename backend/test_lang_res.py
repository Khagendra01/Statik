from typing import Annotated, Dict, TypedDict
from langgraph.graph import Graph
import operator
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
import ast
import sys
from io import StringIO

# Define the state schema
class AgentState(TypedDict):
    messages: list
    code: str
    result: str

# Function to generate Python code using AI
def generate_code(state: AgentState) -> AgentState:
    llm = ChatOpenAI(model="gpt-4", api_key='sk-proj-\-')
    messages = state["messages"]
    
    # Prompt the AI to generate Python code
    response = llm.invoke(
        [
            HumanMessage(content="""You are a Python programmer. Generate Python code to solve the following mathematical problem. 
            Only provide the code without any explanation or markdown formatting.
            The code should print the answers.
            """),
            HumanMessage(content=messages[-1].content)
        ]
    )
    
    state["code"] = response.content
    return state

# Function to execute the generated Python code
def execute_code(state: AgentState) -> AgentState:
    try:
        # Create string buffer to capture stdout
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()

        # Execute the code
        exec(state["code"])
        
        # Get the output
        sys.stdout = old_stdout
        state["result"] = redirected_output.getvalue().strip()
        
    except Exception as e:
        state["result"] = f"Error executing code: {str(e)}"
    
    return state

# Function to check if we should continue
def should_continue(state: AgentState) -> str:
    return "end"

# Create the workflow
def create_math_solver() -> Graph:
    # Define the nodes
    workflow = Graph()

    # Add nodes
    workflow.add_node("generate_code", generate_code)
    workflow.add_node("execute_code", execute_code)

    # Define the end state
    def end_state(state: AgentState) -> AgentState:
        return state

    # Add the end node
    workflow.add_node("end", end_state)

    # Add edges
    workflow.add_edge("generate_code", "execute_code")
    workflow.add_edge("execute_code", "end")

    # Set entry point
    workflow.set_entry_point("generate_code")

    return workflow

# Function to solve math problem
def solve_math_problem(question: str) -> str:
    # Create the graph
    workflow = create_math_solver()
    
    # Compile the graph
    app = workflow.compile()
    
    # Initialize the state
    state = {
        "messages": [HumanMessage(content=question)],
        "code": "",
        "result": ""
    }
    
    try:
        # Run the graph and get the final state
        final_state = app.invoke(state)
        if final_state is None:
            return "Error: Graph execution returned None"
            
        # Print the state for debugging
        print("Final state:", final_state)
        
        return final_state["result"]
    except Exception as e:
        return f"Error executing graph: {str(e)}"

# Example usage
if __name__ == "__main__":
    question = "Calculate the sum of numbers from 1 to 100"
    result = solve_math_problem(question)
    print(f"Question: {question}")
    print(f"Result: {result}")
