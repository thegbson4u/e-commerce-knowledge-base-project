import json
import networkx as nx

def build_knowledge_graph(json_path: str) -> nx.DiGraph:
    """
    Reads the dataset and builds a directional Knowledge Graph.
    Nodes store type and attributes. Edges represent semantic relationships.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    G = nx.DiGraph()
    
    # 1. Create Nodes
    for p in data["products"]:
        G.add_node(p["id"], type="Product", name=p["name"], price=p["price"])
    for b in data["brands"]:
        G.add_node(b["id"], type="Brand", name=b["name"])
    for c in data["categories"]:
        G.add_node(c["id"], type="Category", name=c["name"])
    for v in data["vendors"]:
        G.add_node(v["id"], type="Vendor", name=v["name"])
    for cu in data["customers"]:
        G.add_node(cu["id"], type="Customer", name=cu["name"])
    for o in data["orders"]:
        G.add_node(o["id"], type="Order", date=o["date"])
        
    # 2. Create Semantic Edges
    for p in data["products"]:
        # Product -> MADE_BY -> Brand
        G.add_edge(p["id"], p["brand_id"], type="MADE_BY")
        # Product -> BELONGS_TO -> Category
        G.add_edge(p["id"], p["category_id"], type="BELONGS_TO")
        # Vendor -> SUPPLIES -> Product
        G.add_edge(p["vendor_id"], p["id"], type="SUPPLIES")
        
    for o in data["orders"]:
        # Customer -> PLACED -> Order
        G.add_edge(o["customer_id"], o["id"], type="PLACED")
        for pid in o["product_ids"]:
            # Order -> CONTAINS -> Product
            G.add_edge(o["id"], pid, type="CONTAINS")
            
    return G