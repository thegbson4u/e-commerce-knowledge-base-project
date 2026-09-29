import networkx as nx

def find_node_by_name_and_type(G: nx.DiGraph, name: str, node_type: str):
    """Helper to find the first node matching a specific name and type."""
    if not name:
        return None
    for n, data in G.nodes(data=True):
        if data.get("type") == node_type and data.get("name", "").lower() == name.lower():
            return n
    return None

def get_products_by_brand_and_vendor(G: nx.DiGraph, brand_name: str, vendor_name: str) -> str:
    brand_node = find_node_by_name_and_type(G, brand_name, "Brand")
    vendor_node = find_node_by_name_and_type(G, vendor_name, "Vendor")
    
    if not brand_node or not vendor_node:
        return f"Could not find Brand '{brand_name}' or Vendor '{vendor_name}' in the graph."
    
    products = []
    # Vendor -> SUPPLIES -> Product -> MADE_BY -> Brand
    for _, prod_node, edge_data in G.out_edges(vendor_node, data=True):
        if edge_data.get("type") == "SUPPLIES":
            # Check if this product is made by the target brand
            if G.has_edge(prod_node, brand_node) and G[prod_node][brand_node].get("type") == "MADE_BY":
                products.append(G.nodes[prod_node].get("name", "Unknown"))
                
    if products:
        return f"Products from {brand_name} supplied by {vendor_name}: " + ", ".join(products)
    return f"No products match Brand '{brand_name}' and Vendor '{vendor_name}'."

def get_customer_purchases(G: nx.DiGraph, customer_name: str) -> str:
    cust_node = find_node_by_name_and_type(G, customer_name, "Customer")
    if not cust_node:
        return f"Customer '{customer_name}' not found."
        
    purchased_products = []
    # Customer -> PLACED -> Order -> CONTAINS -> Product
    for _, order_node, e1 in G.out_edges(cust_node, data=True):
        if e1.get("type") == "PLACED":
            for _, prod_node, e2 in G.out_edges(order_node, data=True):
                if e2.get("type") == "CONTAINS":
                    purchased_products.append(G.nodes[prod_node].get("name", "Unknown"))
                    
    if purchased_products:
        return f"Products purchased by {customer_name}: " + ", ".join(purchased_products)
    return f"{customer_name} has not purchased any products."

def get_products_by_category(G: nx.DiGraph, category_name: str) -> str:
    cat_node = find_node_by_name_and_type(G, category_name, "Category")
    if not cat_node:
        return f"Category '{category_name}' not found."
        
    products = []
    for prod_node, _, e in G.in_edges(cat_node, data=True):
        if e.get("type") == "BELONGS_TO":
            products.append(G.nodes[prod_node].get("name", "Unknown"))
            
    if products:
        return f"Products in category {category_name}: " + ", ".join(products)
    return f"No products found in category {category_name}."

def get_vendor_for_product(G: nx.DiGraph, product_name: str) -> str:
    prod_node = find_node_by_name_and_type(G, product_name, "Product")
    if not prod_node:
        return f"Product '{product_name}' not found."
        
    vendors = []
    for vendor_node, _, e in G.in_edges(prod_node, data=True):
        if e.get("type") == "SUPPLIES":
            vendors.append(G.nodes[vendor_node].get("name", "Unknown"))
            
    if vendors:
        return f"Vendors supplying {product_name}: " + ", ".join(vendors)
    return f"No vendor information found for {product_name}."

def retrieve_banana_information(G: nx.DiGraph) -> str:
    """Special retrieval intent directly satisfying the exact-5 banana requirement."""
    banana_nodes = []
    for n, data in G.nodes(data=True):
        # Check all string attributes of the node for the substring 'banana'
        for k, v in data.items():
            if isinstance(v, str) and "banana" in v.lower():
                banana_nodes.append(f"{data.get('type')}: {data.get('name')}")
                break # Only count node once per extraction
                
    if banana_nodes:
        return "Entities containing 'banana':\n- " + "\n- ".join(banana_nodes)
    return "No banana-related entities found."

def execute_graph_query(G: nx.DiGraph, query_intent: dict) -> str:
    """Routes the parsed LLM intent to the specific NetworkX graph traversal logic."""
    intent = query_intent.get("intent", "unknown")
    
    try:
        if intent == "products_by_brand_and_vendor":
            return get_products_by_brand_and_vendor(G, query_intent.get("brand"), query_intent.get("vendor"))
            
        elif intent == "customer_orders":
            return get_customer_purchases(G, query_intent.get("customer"))
            
        elif intent == "products_by_category":
            return get_products_by_category(G, query_intent.get("category"))
            
        elif intent == "vendor_for_product":
            return get_vendor_for_product(G, query_intent.get("product"))
            
        elif intent == "banana_related_retrieval":
            return retrieve_banana_information(G)
            
        else:
            return "Query intent not recognized or supported by the Knowledge Graph."
    except Exception as e:
        return f"Error executing graph traversal: {str(e)}"