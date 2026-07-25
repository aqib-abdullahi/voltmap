// count all asset types
MATCH (n)
RETURN labels(n)[0] AS AssetType,
        count(*) AS count
ORDER BY AssetType;

//count relationship types
MATCH ()-[r]->()
RETURN type(r) AS Relationship,
        count(*) AS Count;

//Verify  every transformer supplies at least one customer
MATCH (t:Transformer)
OPTIONAL MATCH (t)-[:SUPPLIES]->(c:Customer)
RETURN t.id,
        count(c) AS Customers;

//Verifies every customer has exactly one customer
MATCH (c:Customer)
OPTIONAL MATCH (t:Transformer)-[:SUPPLIES]->(c)
RETURN c.id,
        count(t) AS TransformerCount;

//verify every feeder belongs to one substation
MATCH (f:Feeder)
OPTIONAL MATCH (s:Substation)-[:FEEDS]->(f)
RETURN f.id,
        count(s) AS Substations;

//verify no isolated nnodes exist
MATCH (n)
WHERE NOT (n)--()
RETURN labels(n), n.id;