import os
import sys
from dotenv import load_dotenv

# Add parent dir to path to allow running directly from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.graph import build_knowledge_graph
from src.retrieval import execute_graph_query
from src.llm import extract_structured_intent, generate_grounded_answer

def run_pipeline(question: str, graph):
    print(f"\nUser: {question}")
    
    try:
        # Step 1: LLM determines structured intent
        intent_json = extract_structured_intent(question)
        print(f"[DEBUG] Intent generated: {intent_json}")
        
        # Step 2: Python / NetworkX retrieves exact facts deterministically
        retrieved_data = execute_graph_query(graph, intent_json)
        print(f"[DEBUG] Graph retrieval output:\n  {retrieved_data}")
        
        # Step 3: LLM synthesizes grounded final answer
        final_answer = generate_grounded_answer(question, retrieved_data)
        print(f"\nSystem:\n{final_answer}\n")
        print("-" * 50)
        
    except Exception as e:
        print(f"\n[ERROR] Pipeline failed: {str(e)}")

def main():
    load_dotenv()
    
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "ecommerce_data.json")
    print("Initializing Knowledge Graph...")
    graph = build_knowledge_graph(data_path)
    print(f"Graph loaded with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges.\n")
    print("=" * 50)
    
    sample_questions = [
        "Which products from Brand TechCorp are supplied by Vendor ElectroHub?",
        "Which products did Customer Alice purchase?",
        "Which products belong to the Clothing category?",
        "Which vendor supplies the Blender 2000?",
        "Find all information related to the banana nodes."
    ]
    
    # Run through automated examples
    for sq in sample_questions:
        run_pipeline(sq, graph)
        
    # Optional interactive loop
    while True:
        user_input = input("Ask a question (or type 'quit' to exit): ")
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
        if user_input.strip():
            run_pipeline(user_input, graph)

if __name__ == "__main__":
    main()