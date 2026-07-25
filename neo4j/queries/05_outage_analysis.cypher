//Customers affected by transformer failure
MATCH (t:Transformer {id:"TR002"})-[:SUPPLIES]->(c:Customer)
RETURN
    c.id,
    c.name,
    c.customer_type,
    c.load_kW;

//total interrupted load
MATCH (t:Transformer {id:"TR002"})-[:SUPPLIES]->(c:Customer)
RETURN
    t.id,
    count(c) AS Customers_Affected,
    round(sum(c.load_kW),2) AS Interrupted_Load_kW;

//Customers downstream of a switch
MATCH (sw:Switch {id:"SW003"})
      -[:CONNECTED_TO*]->(:Transformer)
      -[:SUPPLIES]->(c:Customer)
RETURN
    c.id,
    c.name,
    c.customer_type
ORDER BY c.id;

//transformers isolated by a switch
MATCH (sw:Switch {id:"SW003"})
      -[:CONNECTED_TO*]->(t:Transformer)
RETURN
    t.id,
    t.rating_kVA;

//counts customers lost due to a switch operation
MATCH (sw:Switch {id:"SW003"})
      -[:CONNECTED_TO*]->(:Transformer)
      -[:SUPPLIES]->(c:Customer)
RETURN
    count(c) AS Customers_Affected;

//interrupted load by customer type
MATCH (sw:Switch {id:"SW003"})
      -[:CONNECTED_TO*]->(:Transformer)
      -[:SUPPLIES]->(c:Customer)
RETURN
    c.customer_type,
    round(sum(c.load_kW),2) AS Interrupted_Load_kW
ORDER BY Interrupted_Load_kW DESC;

//Highest impact tranformer failuure
MATCH (sw:Switch {id:"SW003"})
      -[:CONNECTED_TO*]->(:Transformer)
      -[:SUPPLIES]->(c:Customer)
RETURN
    c.customer_type,
    round(sum(c.load_kW),2) AS Interrupted_Load_kW
ORDER BY Interrupted_Load_kW DESC;

//Highest impacct switch
MATCH (sw:Switch)
OPTIONAL MATCH (sw)-[:CONNECTED_TO*]->(:Transformer)-[:SUPPLIES]->(c:Customer)
RETURN
    sw.id,
    count(DISTINCT c) AS Customers_Affected,
    round(sum(c.load_kW),2) AS Interrupted_Load_kW
ORDER BY Interrupted_Load_kW DESC;

