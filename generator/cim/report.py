from .mapping import cim_entity


class CIMReport:
    
    def generate(self, network):
        print("=" * 50)
        print("VoltMap CIM Profile")
        print("=" * 50)
        
        collections = [
            network.substations,
            network.feeders,
            network.line_segments,
            network.poles,
            network.switches,
            network.transformers,
            network.customers,
        ]
        
        for collection in collections:
            if not collection:
                continue
            
            entity = cim_entity(collection[0])
            
            print(
                f"{entity.name:<20} {len(collection):>8}"
            )
        