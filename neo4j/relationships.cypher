// voltmap Relationships

// Substation -> Feeders
MATCH (ss:Substation {id:"SS001"})
MATCH (f1:Feeder {id:"F001"})
MATCH (f2:Feeder {id:"F002"})

MERGE (ss)-[:FEEDS]->(f1)
MERGE (ss)-[:FEEDS]->(f2);

// Feeders -> Switches
MATCH (f1:Feeder {id:"F001"})
MATCH (f2:Feeder {id:"F002"})
MATCH (sw1:Switch {id:"SW001"})
MATCH (sw2:Switch {id:"SW002"})
MATCH (sw3:Switch {id:"SW003"})
MATCH (sw4:Switch {id:"SW004"})

MERGE (f1)-[:CONNECTED_TO]->(sw1)
MERGE (f1)-[:CONNECTED_TO]->(sw2)
MERGE (f2)-[:CONNECTED_TO]->(sw3)
MERGE (f2)-[:CONNECTED_TO]->(sw4);

// Switches -> Transformers
MATCH (sw1:Switch {id:"SW001"})
MATCH (sw2:Switch {id:"SW002"})
MATCH (sw3:Switch {id:"SW003"})
MATCH (sw4:Switch {id:"SW004"})

MATCH (tr1:Transformer {id:"TR001"})
MATCH (tr2:Transformer {id:"TR002"})
MATCH (tr3:Transformer {id:"TR003"})
MATCH (tr4:Transformer {id:"TR004"})

MERGE (sw1)-[:CONNECTED_TO]->(tr1)
MERGE (sw2)-[:CONNECTED_TO]->(tr2)
MERGE (sw3)-[:CONNECTED_TO]->(tr3)
MERGE (sw4)-[:CONNECTED_TO]->(tr4);

//verify
//MATCH (n)-[r]->(m)
//RETURN n, r, m;