// VoltMap Dataset v1.0
// Relationship Definitions
//runs after constraints.cypher and data.cypher
// SUBSTATION -> FEEDERS
MATCH (s:Substation {id:"SS001"})
MATCH (f1:Feeder {id:"F001"})
MATCH (f2:Feeder {id:"F002"})

MERGE (s)-[r1:FEEDS]->(f1)
SET
    r1.nominal_voltage_kV = 11,
    r1.connection_type = "OUTGOING_FEEDER",
    r1.status = "ENERGIZED";

MERGE (s)-[r2:FEEDS]->(f2)
SET
    r2.nominal_voltage_kV = 11,
    r2.connection_type = "OUTGOING_FEEDER",
    r2.status = "ENERGIZED";

// NORTH FEEDER NETWORK
MATCH (f:Feeder {id:"F001"})
MATCH (sw1:Switch {id:"SW001"})
MATCH (sw2:Switch {id:"SW002"})
MATCH (tr1:Transformer {id:"TR001"})
MATCH (tr2:Transformer {id:"TR002"})

MERGE (f)-[r:CONNECTED_TO]->(sw1)
SET
    r.connection_type = "MV_LINE",
    r.nominal_voltage_kV = 11,
    r.length_m = 250,
    r.status = "ENERGIZED";
MERGE (sw1)-[r:CONNECTED_TO]->(sw2)
SET
    r.connection_type = "MV_LINE",
    r.nominal_voltage_kV = 11,
    r.length_m = 180,
    r.status = "ENERGIZED";
MERGE (sw1)-[r:CONNECTED_TO]->(tr1)
SET
    r.connection_type = "SERVICE_CONNECTION",
    r.nominal_voltage_kV = 11,
    r.length_m = 35,
    r.status = "ENERGIZED";
MERGE (sw2)-[r:CONNECTED_TO]->(tr2);
SET
    r.connection_type = "SERVICE_CONNECTION",
    r.nominal_voltage_kV = 11,
    r.length_m = 35,
    r.status = "ENERGIZED";

// SOUTH FEEDER NETWORK

MATCH (f:Feeder {id:"F002"})
MATCH (sw3:Switch {id:"SW003"})
MATCH (sw4:Switch {id:"SW004"})
MATCH (tr3:Transformer {id:"TR003"})
MATCH (tr4:Transformer {id:"TR004"})

MERGE (f)-[r:CONNECTED_TO]->(sw3)
SET
    r.connection_type = "MV_LINE",
    r.nominal_voltage_kV = 11,
    r.length_m = 250,
    r.status = "ENERGIZED";
MERGE (sw3)-[:CONNECTED_TO]->(sw4)
SET
    r.connection_type = "MV_LINE",
    r.nominal_voltage_kV = 11,
    r.length_m = 250,
    r.status = "ENERGIZED";
MERGE (sw3)-[:CONNECTED_TO]->(tr3)
SET
    r.connection_type = "SERVICE_CONNECTION",
    r.nominal_voltage_kV = 11,
    r.length_m = 35,
    r.status = "ENERGIZED";
MERGE (sw4)-[:CONNECTED_TO]->(tr4);
SET
    r.connection_type = "SERVICE_CONNECTION",
    r.nominal_voltage_kV = 11,
    r.length_m = 35,
    r.status = "ENERGIZED";

// TRANSFORMER to CUSTOMERS
UNWIND [

["TR001","C001"],
["TR001","C002"],
["TR001","C003"],
["TR001","C004"],
["TR001","C005"],

["TR002","C006"],
["TR002","C007"],
["TR002","C008"],
["TR002","C009"],
["TR002","C010"],

["TR003","C011"],
["TR003","C012"],
["TR003","C013"],
["TR003","C014"],
["TR003","C015"],

["TR004","C016"],
["TR004","C017"],
["TR004","C018"],
["TR004","C019"],
["TR004","C020"]

] AS pair

MATCH (t:Transformer {id: pair[0]})
MATCH (c:Customer {id: pair[1]})

MERGE (t)-[:SUPPLIES]->(c);
SET
    r.service_voltage_kV = 0.415,
    r.phase = "3P",
    r.service_status = "ACTIVE";


// VERIFICATION
// Count relationships by type
MATCH ()-[r]->()
RETURN
type(r) AS Relationship,
count(*) AS Count
ORDER BY Relationship;



// Total relationship count
MATCH ()-[r]->()
RETURN count(r) AS TotalRelationships;

// Visualize the complete network
MATCH p=(:Substation)-[*]->(:Customer)
RETURN p;