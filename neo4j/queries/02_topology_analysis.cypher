//Trace entire supply path
MATCH p=(s:Substation)-[:FEEDS|CONNECTED_TO|SUPPLIES*]->(c:Customer)
RETURN p;

//find all customers on a feeder
MATCH (:Substation)-[:FEEDS]->(f:Feeder {id:"F001"})
      -[:CONNECTED_TO*]->(:Transformer)-[:SUPPLIES]->(c:Customer)
RETURN c.id,
       c.name,
       c.customer_type,
       c.load_kW
ORDER BY c.id;

//finde evry transformer on a feeder
MATCH (:Feeder {id:"F001"})
      -[:CONNECTED_TO*]->(t:Transformer)
RETURN t.id,
       t.rating_kVA;
    
//trace upstream supply path
MATCH p=(c:Customer {id:"C018"})<-[:SUPPLIES]-(:Transformer)
        <-[:CONNECTED_TO*]-(:Feeder)
        <-[:FEEDS]-(:Substation)
RETURN p;