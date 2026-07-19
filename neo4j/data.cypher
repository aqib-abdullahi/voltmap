// voltmap dataset v1.0
// nodes Only

// Substation 
MERGE (:Substation {
    id: "SS001",
    name: "Jimeta Distribution Substation",
    voltage_kV: 33,
    location: "Jimeta, Adamawa"
});

// Feeders
MERGE (:Feeder {
    id: "F001",
    name: "North Feeder",
    voltage_kV: 11,
    length_km: 12.4
});

MERGE (:Feeder {
    id: "F002",
    name: "South Feeder",
    voltage_kV: 11,
    length_km: 10.8
});

// Switches
MERGE (:Switch {
    id: "SW001",
    type: "Load Break Switch",
    status: "CLOSED"
});

MERGE (:Switch {
    id: "SW002",
    type: "Load Break Switch",
    status: "CLOSED"
});

MERGE (:Switch {
    id: "SW003",
    type: "Load Break Switch",
    status: "CLOSED"
});

MERGE (:Switch {
    id: "SW004",
    type: "Load Break Switch",
    status: "CLOSED"
});

// Transformers
MERGE (:Transformer {
    id: "TR001",
    rating_kVA: 300,
    primary_voltage: 11,
    secondary_voltage: 0.415
});

MERGE (:Transformer {
    id: "TR002",
    rating_kVA: 500,
    primary_voltage: 11,
    secondary_voltage: 0.415
});

MERGE (:Transformer {
    id: "TR003",
    rating_kVA: 300,
    primary_voltage: 11,
    secondary_voltage: 0.415
});

MERGE (:Transformer {
    id: "TR004",
    rating_kVA: 500,
    primary_voltage: 11,
    secondary_voltage: 0.415
});

//verify
//MATCH (n)
//RETURN labels(n), count(*)
//ORDER BY labels(n);