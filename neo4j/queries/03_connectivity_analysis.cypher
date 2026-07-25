//custormer supply path
MATCH p=(s:Substation)-[:FEEDS|CONNECTED_TO|SUPPLIES*]->(c:Customer {id:"C018"})
RETURN p;

//allc cutomer supplied by a feeder
MATCH (:Feeder {id:"F001"})
      -[:CONNECTED_TO*]->(:Transformer)
      -[:SUPPLIES]->(c:Customer)
RETURN c.id,
       c.name
ORDER BY c.id;

//all transformers fed by a substation
MATCH (:Substation {id:"SS001"})
      -[:FEEDS|CONNECTED_TO*]->(t:Transformer)
RETURN t.id,
       t.rating_kVA;

//checks is every customer connected?
MATCH (c:Customer)
WHERE NOT EXISTS {
    MATCH (:Substation)-[:FEEDS|CONNECTED_TO|SUPPLIES*]->(c)
}
RETURN c.id,
       c.name;

//Isolated assets
MATCH (n)
WHERE NOT (n)--()
RETURN labels(n)[0] AS AssetType,
       n.id;

//Count customers served by each feeder
MATCH (f:Feeder)
OPTIONAL MATCH (f)-[:CONNECTED_TO*]->(:Transformer)-[:SUPPLIES]->(c:Customer)
RETURN f.id,
       count(c) AS Customers;

//count customers served by each transformer
MATCH (t:Transformer)
OPTIONAL MATCH (t)-[:SUPPLIES]->(c:Customer)
RETURN t.id,
       count(c) AS Customers
ORDER BY t.id;

//fiind assets downstream of a feeder
MATCH (f:Feeder {id:"F002"})
MATCH (f)-[:CONNECTED_TO|SUPPLIES*]->(n)
RETURN DISTINCT
       labels(n)[0] AS AssetType,
       n.id
ORDER BY AssetType, n.id;

