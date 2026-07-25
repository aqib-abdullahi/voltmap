//total load per transformer
MATCH (t:Transformer)-[:SUPPLIES]->(c:Customer)
RETURN
    t.id AS Transformer,
    t.rating_kVA AS Rating_kVA,
    round(sum(c.load_kW),2) AS Connected_Load_kW
ORDER BY Connected_Load_kW DESC;

//transforemer loading %
MATCH (t:Transformer)-[:SUPPLIES]->(c:Customer)
WITH t,
     sum(c.load_kW) AS load
RETURN
    t.id,
    t.rating_kVA,
    round(load,2) AS Connected_Load_kW,
    round((load / t.rating_kVA) * 100,2) AS Loading_Percentage
ORDER BY Loading_Percentage DESC;

//total load per feeder
MATCH (f:Feeder)-[:CONNECTED_TO*]->(:Transformer)-[:SUPPLIES]->(c:Customer)
RETURN
    f.id,
    round(sum(c.load_kW),2) AS Total_Load_kW
ORDER BY Total_Load_kW DESC;

//total load by cutomer type
MATCH (c:Customer)
RETURN
    c.customer_type,
    round(sum(c.load_kW),2) AS Total_Load_kW
ORDER BY Total_Load_kW DESC;

//average residential load
MATCH (c:Customer)
WHERE c.customer_type = "Residential"
RETURN
    round(avg(c.load_kW),2) AS Average_Residential_Load_kW;

//largest individual loads
MATCH (c:Customer)
RETURN
    c.name,
    c.customer_type,
    c.load_kW
ORDER BY c.load_kW DESC
LIMIT 10;

//load distribution across transformers
MATCH (t:Transformer)-[:SUPPLIES]->(c:Customer)
RETURN
    t.id,
    count(c) AS Customers,
    round(avg(c.load_kW),2) AS Average_Load_kW,
    round(max(c.load_kW),2) AS Peak_Load_kW,
    round(sum(c.load_kW),2) AS Total_Load_kW;

//Network connected load
MATCH (c:Customer)
RETURN
    round(sum(c.load_kW),2) AS Total_Network_Load_kW;