//most heavily loaded transformer
MATCH (t:Transformer)-[:SUPPLIES]->(c:Customer)
RETURN
    t.id,
    round(sum(c.load_kW),2) AS Connected_Load_kW
ORDER BY Connected_Load_kW DESC
LIMIT 1;

//most heavily loaded feeder
MATCH (f:Feeder)-[:CONNECTED_TO*]->(:Transformer)-[:SUPPLIES]->(c:Customer)
RETURN
    f.id,
    round(sum(c.load_kW),2) AS Connected_Load_kW
ORDER BY Connected_Load_kW DESC
LIMIT 1;

//largest customer
MATCH (c:Customer)
RETURN
    c.name,
    c.customer_type,
    c.load_kW
ORDER BY c.load_kW DESC
LIMIT 5;

//transformers above a loading threshold
MATCH (t:Transformer)-[:SUPPLIES]->(c:Customer)
WITH
    t,
    sum(c.load_kW) AS Load
WHERE (Load / t.rating_kVA) * 100 > 80
RETURN
    t.id,
    t.rating_kVA,
    round(Load,2) AS Load_kW,
    round((Load / t.rating_kVA) * 100,2) AS Loading_Percentage;

//Commercial customers on a feeder
MATCH (:Feeder {id:"F001"})
      -[:CONNECTED_TO*]->(:Transformer)
      -[:SUPPLIES]->(c:Customer)
WHERE c.customer_type = "Commercial"
RETURN
    c.name,
    c.load_kW;

//assets by voltage level
MATCH (s:Substation)
RETURN "Substation" AS Asset,
       s.voltage_kV AS Voltage

UNION ALL

MATCH (f:Feeder)
RETURN "Feeder",
       f.voltage_kV;