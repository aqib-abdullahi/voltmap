// VoltMap Dataset v1.0

// OPTIONAL: CLEAR DB
// remove comment for fresh import.
// MATCH (n) DETACH DELETE n;

// SUBSTATIONS
MERGE (:Substation {
    id: "SS001",
    name: "Jimeta Distribution Substation",
    voltage_kV: 33,
    location: "Jimeta, Adamawa"
});

// FEEDERS
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


// SWITCHES
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

// TRANSFORMERS
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


// LINES
MERGE (:LineSegment {
    id:"LS001",
    name:"North Main Line 1",
    voltage_kV:11,
    length_m:250,
    conductor_type:"AAC",
    conductor_size_mm2: 100,
    status:"ENERGIZED"
});

MERGE (:LineSegment {
    id:"LS002",
    name:"North Main Line 2",
    voltage_kV:11,
    length_m:180,
    conductor_type:"AAC",
    conductor_size_mm2: 100,
    status:"ENERGIZED"
});

MERGE (:LineSegment {
    id:"LS003",
    name:"North Transformer Spur",
    voltage_kV:11,
    length_m:40,
    conductor_type:"AAC",
    conductor_size_mm2: 100,
    status:"ENERGIZED"
});

MERGE (:LineSegment {
    id:"Ls004",
    name:"South Line 1",
    voltage_kV:11,
    length_m:220,
    conductor_type:"AAC",
    conductor_size_mm2: 100,
    status:"ENERGIZED"
});

MERGE (:LineSegment {
    id:"LS005",
    name:"South Line 2",
    voltage_kV:11,
    length_m:170,
    conductor_type:"AAC",
    conductor_size_mm2: 100,
    status:"ENERGIZED"
});

MERGE (:LineSegment {
    id:"LS006",
    name:"South Transformer Spur",
    voltage_kV:11,
    length_m:35,
    conductor_type:"AAC",
    conductor_size_mm2: 100,
    status:"ENERGIZED"
});


// POLES
MERGE (:Pole {
    id:"P001",
    pole_number:"JP-001",
    material:"Concrete",
    height_m:12,
    installation_year:2021
});

MERGE (:Pole {
    id:"P002",
    pole_number:"JP-002",
    material:"Concrete",
    height_m:12,
    installation_year:2021
});

MERGE (:Pole {
    id:"P003",
    pole_number:"JP-003",
    material:"Concrete",
    height_m:12,
    installation_year:2021
});

MERGE (:Pole {
    id:"P004",
    pole_number:"JP-004",
    material:"Concrete",
    height_m:12,
    installation_year:2021
});

// CUSTOMERS
UNWIND [

    // Transformer TR001
    {id:"C001", name:"Residence A", type:"Residential", load:2.5, transformer:"TR001"},
    {id:"C002", name:"Residence B", type:"Residential", load:3.1, transformer:"TR001"},
    {id:"C003", name:"Pharmacy", type:"Commercial", load:8.2, transformer:"TR001"},
    {id:"C004", name:"Primary School", type:"Institutional", load:18.0, transformer:"TR001"},
    {id:"C005", name:"Health Centre", type:"Healthcare", load:15.4, transformer:"TR001"},

    // Transformer TR002
    {id:"C006", name:"Residence C", type:"Residential", load:2.8, transformer:"TR002"},
    {id:"C007", name:"Residence D", type:"Residential", load:3.5, transformer:"TR002"},
    {id:"C008", name:"Bakery", type:"Commercial", load:9.1, transformer:"TR002"},
    {id:"C009", name:"Mosque", type:"Religious", load:7.8, transformer:"TR002"},
    {id:"C010", name:"Water Works", type:"Utility", load:22.5, transformer:"TR002"},

    // Transformer TR003
    {id:"C011", name:"Residence E", type:"Residential", load:2.4, transformer:"TR003"},
    {id:"C012", name:"Residence F", type:"Residential", load:2.9, transformer:"TR003"},
    {id:"C013", name:"Supermarket", type:"Commercial", load:16.8, transformer:"TR003"},
    {id:"C014", name:"Secondary School", type:"Institutional", load:24.2, transformer:"TR003"},
    {id:"C015", name:"Clinic", type:"Healthcare", load:13.7, transformer:"TR003"},

    // Transformer TR004
    {id:"C016", name:"Residence G", type:"Residential", load:2.6, transformer:"TR004"},
    {id:"C017", name:"Residence H", type:"Residential", load:3.2, transformer:"TR004"},
    {id:"C018", name:"Hotel", type:"Commercial", load:28.5, transformer:"TR004"},
    {id:"C019", name:"Filling Station", type:"Commercial", load:19.6, transformer:"TR004"},
    {id:"C020", name:"Local Government Office", type:"Government", load:31.0, transformer:"TR004"}

] AS customer

MERGE (c:Customer {id: customer.id})
SET
    c.name = customer.name,
    c.customer_type = customer.type,
    c.load_kW = customer.load;

// VERIFICATION
// MATCH (n)
// RETURN
//     labels(n)[0] AS Asset,
//     count(*) AS Count
// ORDER BY Asset;