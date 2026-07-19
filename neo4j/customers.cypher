// VoltMap Dataset v1.0
// Customers

UNWIND [

    // TR001
    {id:"C001", name:"Residence A", type:"Residential", load:2.5, transformer:"TR001"},
    {id:"C002", name:"Residence B", type:"Residential", load:3.1, transformer:"TR001"},
    {id:"C003", name:"Pharmacy", type:"Commercial", load:8.2, transformer:"TR001"},
    {id:"C004", name:"Primary School", type:"Institutional", load:18.0, transformer:"TR001"},
    {id:"C005", name:"Health Centre", type:"Healthcare", load:15.4, transformer:"TR001"},

    // TR002
    {id:"C006", name:"Residence C", type:"Residential", load:2.8, transformer:"TR002"},
    {id:"C007", name:"Residence D", type:"Residential", load:3.5, transformer:"TR002"},
    {id:"C008", name:"Bakery", type:"Commercial", load:9.1, transformer:"TR002"},
    {id:"C009", name:"Mosque", type:"Religious", load:7.8, transformer:"TR002"},
    {id:"C010", name:"Water Works", type:"Utility", load:22.5, transformer:"TR002"},

    // TR003
    {id:"C011", name:"Residence E", type:"Residential", load:2.4, transformer:"TR003"},
    {id:"C012", name:"Residence F", type:"Residential", load:2.9, transformer:"TR003"},
    {id:"C013", name:"Supermarket", type:"Commercial", load:16.8, transformer:"TR003"},
    {id:"C014", name:"Secondary School", type:"Institutional", load:24.2, transformer:"TR003"},
    {id:"C015", name:"Clinic", type:"Healthcare", load:13.7, transformer:"TR003"},

    // TR004
    {id:"C016", name:"Residence G", type:"Residential", load:2.6, transformer:"TR004"},
    {id:"C017", name:"Residence H", type:"Residential", load:3.2, transformer:"TR004"},
    {id:"C018", name:"Hotel", type:"Commercial", load:28.5, transformer:"TR004"},
    {id:"C019", name:"Filling Station", type:"Commercial", load:19.6, transformer:"TR004"},
    {id:"C020", name:"Local Government Office", type:"Government", load:31.0, transformer:"TR004"}

] AS customer

MERGE (c:Customer {id: customer.id})
SET c.name = customer.name,
    c.customer_type = customer.type,
    c.load_kW = customer.load

WITH c, customer
MATCH (t:Transformer {id: customer.transformer})
MERGE (t)-[:SUPPLIES]->(c);