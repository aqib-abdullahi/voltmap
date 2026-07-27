
// VoltMap v1.0
// NODE UNIQUENESS CONSTRAINTS
// Substation
CREATE CONSTRAINT substation_id IF NOT EXISTS
FOR (s:Substation)
REQUIRE s.id IS UNIQUE;

// Feeder
CREATE CONSTRAINT feeder_id IF NOT EXISTS
FOR (f:Feeder)
REQUIRE f.id IS UNIQUE;

// Switch
CREATE CONSTRAINT switch_id IF NOT EXISTS
FOR (sw:Switch)
REQUIRE sw.id IS UNIQUE;

// Transformer
CREATE CONSTRAINT transformer_id IF NOT EXISTS
FOR (t:Transformer)
REQUIRE t.id IS UNIQUE;

// Customer
CREATE CONSTRAINT customer_id IF NOT EXISTS
FOR (c:Customer)
REQUIRE c.id IS UNIQUE;

// PROPERTY EXISTENCE CONSTRAINTS
// Substation
CREATE CONSTRAINT substation_voltage IF NOT EXISTS
FOR (s:Substation)
REQUIRE s.voltage_kV IS NOT NULL;

// Feeder
CREATE CONSTRAINT feeder_voltage IF NOT EXISTS
FOR (f:Feeder)
REQUIRE f.voltage_kV IS NOT NULL;

// Transformer
CREATE CONSTRAINT transformer_rating IF NOT EXISTS
FOR (t:Transformer)
REQUIRE t.rating_kVA IS NOT NULL;

// Customer
CREATE CONSTRAINT customer_load IF NOT EXISTS
FOR (c:Customer)
REQUIRE c.load_kW IS NOT NULL;

// Switch
CREATE CONSTRAINT switch_status IF NOT EXISTS
FOR (sw:Switch)
REQUIRE sw.status IS NOT NULL;

// INDEXES
// Frequently searched assets
CREATE INDEX substation_name IF NOT EXISTS
FOR (s:Substation)
ON (s.name);

CREATE INDEX feeder_name IF NOT EXISTS
FOR (f:Feeder)
ON (f.name);

CREATE INDEX customer_name IF NOT EXISTS
FOR (c:Customer)
ON (c.name);

CREATE INDEX customer_type IF NOT EXISTS
FOR (c:Customer)
ON (c.customer_type);

CREATE INDEX transformer_rating IF NOT EXISTS
FOR (t:Transformer)
ON (t.rating_kVA);


// VERIFY
SHOW CONSTRAINTS;
SHOW INDEXES;