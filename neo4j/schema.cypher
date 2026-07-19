// voltmap graph schema v1.0

//substations

CREATE (ss:Substation {
    id: "SS001",
    name: "Jimeta distribution substation",
    voltage_kV: 33,
    location: "Jimeta"
});

// feeders
CREATE (f1:Feeder {
    id: "F001",
    name: "North Feeder",
    voltage_kV: 11,
    length_km: 12.4
});

CREATE (f2:Feeder {
    id: "F002",
    name: "South Feeder",
    voltage_kV: 11,
    length_km: 10.8
});

// connecting feeders

MATCH (ss:Substation {id:"SS001"})
MATCH (f1:Feeder {id:"F001"})
MATCH (f2:Feeder {id:"F002"})

CREATE (ss)-[:FEEDS]->(f1)
CREATE (ss)-[:FEEDS]->(f2);