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