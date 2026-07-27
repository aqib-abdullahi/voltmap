// VoltMap Constraints

CREATE CONSTRAINT substation_id
                IF NOT EXISTS
                FOR (n:Substation)
                REQUIRE n.id IS UNIQUE;
                
CREATE CONSTRAINT feeder_id
                IF NOT EXISTS
                FOR (n:Feeder)
                REQUIRE n.id IS UNIQUE;
                
CREATE CONSTRAINT linesegment_id
                IF NOT EXISTS
                FOR (n:LineSegment)
                REQUIRE n.id IS UNIQUE;
                
CREATE CONSTRAINT pole_id
                IF NOT EXISTS
                FOR (n:Pole)
                REQUIRE n.id IS UNIQUE;
                
CREATE CONSTRAINT switch_id
                IF NOT EXISTS
                FOR (n:Switch)
                REQUIRE n.id IS UNIQUE;
                
CREATE CONSTRAINT transformer_id
                IF NOT EXISTS
                FOR (n:Transformer)
                REQUIRE n.id IS UNIQUE;
                
CREATE CONSTRAINT customer_id
                IF NOT EXISTS
                FOR (n:Customer)
                REQUIRE n.id IS UNIQUE;
                