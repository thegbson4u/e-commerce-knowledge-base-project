# Sample Questions & Expected Outputs

**1. Which products from Brand TechCorp are supplied by Vendor ElectroHub?**
* **Expected Intent:** `{"intent": "products_by_brand_and_vendor", "brand": "TechCorp", "vendor": "ElectroHub"}`
* **Expected Graph Retrieval:** Laptop X1, Smartphone Y, Wireless Mouse
* **Expected Answer:** TechCorp products supplied by ElectroHub include the Laptop X1, Smartphone Y, and Wireless Mouse.

**2. Which products did Customer Alice purchase?**
* **Expected Intent:** `{"intent": "customer_orders", "customer": "Alice"}`
* **Expected Graph Retrieval:** Laptop X1, Wireless Mouse, Desk Chair
* **Expected Answer:** Alice purchased a Laptop X1, Wireless Mouse, and a Desk Chair.

**3. Which products belong to the Clothing category?**
* **Expected Intent:** `{"intent": "products_by_category", "category": "Clothing"}`
* **Expected Graph Retrieval:** Running Shoes, Yoga Mat
* **Expected Answer:** The products in the Clothing category are Running Shoes and a Yoga Mat.

**4. Which vendor supplies the Blender 2000?**
* **Expected Intent:** `{"intent": "vendor_for_product", "product": "Blender 2000"}`
* **Expected Graph Retrieval:** ElectroHub
* **Expected Answer:** The Blender 2000 is supplied by ElectroHub.

**5. Find all information related to the banana nodes.**
* **Expected Intent:** `{"intent": "banana_related_retrieval"}`
* **Expected Graph Retrieval:** (Exact 5 Entities) Organic Banana, Banana Chips, Banana Farms Ltd, Banana Products, Global Banana Suppliers
* **Expected Answer:** The graph contains the following banana-related entities: Product: Organic Banana, Product: Banana Chips, Brand: Banana Farms Ltd, Category: Banana Products, and Vendor: Global Banana Suppliers.