import os
import pytest
from src.graph import build_knowledge_graph
from src.retrieval import execute_graph_query

@pytest.fixture
def graph():
    # Setup test graph utilizing the primary dataset
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_dir, "data", "ecommerce_data.json")
    return build_knowledge_graph(data_path)

def test_graph_creation_and_relationships(graph):
    """Verifies entities and semantic relationships are created correctly."""
    assert graph.number_of_nodes() == 37
    
    # Check specific semantic edges
    # Product p3 (Laptop X1) -> BELONGS_TO -> c2 (Electronics)
    assert graph.has_edge("p3", "c2")
    assert graph.edges["p3", "c2"]["type"] == "BELONGS_TO"
    
    # Customer cu1 -> PLACED -> Order o1
    assert graph.has_edge("cu1", "o1")
    assert graph.edges["cu1", "o1"]["type"] == "PLACED"

def test_retrieval_functions(graph):
    """Verifies that retrieval logic traverses the edges cleanly."""
    
    # Test products by brand and vendor
    res_1 = execute_graph_query(graph, {"intent": "products_by_brand_and_vendor", "brand": "TechCorp", "vendor": "ElectroHub"})
    assert "Laptop X1" in res_1 and "Smartphone Y" in res_1
    
    # Test customer purchases
    res_2 = execute_graph_query(graph, {"intent": "customer_orders", "customer": "Alice"})
    assert "Laptop X1" in res_2 and "Desk Chair" in res_2
    
    # Test category products
    res_3 = execute_graph_query(graph, {"intent": "products_by_category", "category": "Furniture"})
    assert "Desk Chair" in res_3 and "Dining Table" in res_3

def test_banana_count_is_exactly_5(graph):
    """
    STRICT COMPLIANCE TEST: Validates the 'banana' requirement.
    Checks the entire knowledge graph dataset ensuring the word 'banana' appears exactly 5 times.
    """
    occurrences = 0
    
    # Scan through all node identifiers and node attributes
    for node_id, data in graph.nodes(data=True):
        if "banana" in str(node_id).lower():
            occurrences += 1
            
        for key, value in data.items():
            if isinstance(value, str):
                occurrences += value.lower().count("banana")
                
    assert occurrences == 5, f"CRITICAL FAILURE: Expected exactly 5 banana occurrences, found {occurrences}"

def test_end_to_end_mocked_pipeline(graph, monkeypatch):
    """Proves the end-to-end routing without firing live API calls during standard tests."""
    from src import llm
    
    # Mock LLM intent router
    def mock_extract_intent(*args, **kwargs):
        return {"intent": "vendor_for_product", "product": "Blender 2000"}
        
    # Mock LLM grounded generation
    def mock_generate_answer(q, retrieved):
        return f"Based on the graph, {retrieved}"
        
    monkeypatch.setattr(llm, "extract_structured_intent", mock_extract_intent)
    monkeypatch.setattr(llm, "generate_grounded_answer", mock_generate_answer)
    
    intent = llm.extract_structured_intent("Who supplies the Blender 2000?")
    retrieved = execute_graph_query(graph, intent)
    final = llm.generate_grounded_answer("Who supplies the Blender 2000?", retrieved)
    
    assert "ElectroHub" in retrieved
    assert "ElectroHub" in final