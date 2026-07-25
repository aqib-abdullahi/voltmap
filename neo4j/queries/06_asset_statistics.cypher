//counts assets by type
MATCH (n)
RETURN labels(n)[0] AS Asset,
       count(*) AS Count
ORDER BY Asset;

//total connected load
MATCH (c:Customer)
RETURN round(sum(c.load_kW),2) AS Total_Load_kW;

//customer distribution by type
MATCH (c:Customer)
RETURN c.customer_type,
       count(*) AS Customers
ORDER BY Customers DESC;

//transformer by capacity summary
MATCH (t:Transformer)
RETURN
    count(*) AS Transformers,
    round(sum(t.rating_kVA),2) AS Total_Capacity_kVA,
    round(avg(t.rating_kVA),2) AS Average_Capacity_kVA,
    max(t.rating_kVA) AS Largest_Transformer_kVA;

//average customer load
MATCH (c:Customer)
RETURN
    round(avg(c.load_kW),2) AS Average_Load_kW,
    min(c.load_kW) AS Minimum_Load_kW,
    max(c.load_kW) AS Maximum_Load_kW;

//Number of customers per transformer
MATCH (t:Transformer)-[:SUPPLIES]->(c:Customer)
RETURN
    t.id,
    count(c) AS Customers
ORDER BY Customers DESC;

//network summary
MATCH (n)
WITH count(n) AS Nodes
MATCH ()-[r]->()
RETURN
    Nodes,
    count(r) AS Relationships;