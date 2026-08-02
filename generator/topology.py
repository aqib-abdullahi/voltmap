"""
VoltMap Generator
Topology generation engine.
Creates an in-memory electrical distribution network.
"""
from models import (
    Substation,
    Feeder,
    LineSegment,
    Pole,
    Switch,
    Transformer,
    Customer
)
from ids import IDGenerator
import config, rules
import random
from settings import GeneratorConfig
from network import Network

class TopologyGenerator:

    def __init__(self, config=None):
        self.config = GeneratorConfig()
        self.ids = IDGenerator()
        # self.substations = []
        # self.feeders = []
        # self.line_segments = []
        # self.poles = []
        # self.switches = []
        # self.transformers = []
        # self.customers = []
        self.network = Network()
    
    def generate(self):
        for _ in range(self.config.num_substations):
            self._create_substation()

        return self
    
    def _create_substation(self):
        substation = Substation(
            id=self.ids.next("SS"),
            name="Distribution Substation",
            voltage_kV=(self.config.substation_voltage_kv),
            location="Synthetic"
        )
        self.network.substations.append(substation)

        for _ in range(self.config.feeders_per_substation):
            self._create_feeder(substation)

    def _create_feeder(self, substation):
        feeder = Feeder(
            id=self.ids.next("F"),
            name="Feeder",
            voltage_kV=self.config.feeder_voltage_kv,
            length_km=0,
            source=substation
        )
        substation.feeders.append(feeder)
        self.network.feeders.append(feeder)

        # for _ in range(config.LINE_SEGMENTS_PER_FEEDER):
        #     self._create_line_segment(feeder, i + 1)
        for segment_index in range(self.config.line_segments_per_feeder):
            self._create_line_segment(feeder, segment_index + 1)

    def _create_line_segment(self, feeder, segment_index):
        length = random.randint(
            rules.MIN_LINE_LENGTH,
            rules.MAX_LINE_LENGTH
        )
        line = LineSegment(
            id=self.ids.next("LS"),
            name="Line Segment",
            voltage_kV=self.config.feeder_voltage_kv,
            length_m=length,
            conductor_type="AAC",
            conductor_size_mm2=100
        )
        line.feeder = feeder
        feeder.line_segments.append(line)
        self.network.line_segments.append(line)
        self._create_pole(line, segment_index)
        # for pole_index in range(config.POLES_PER_LINE_SEGMENT):
        #     self._create_pole(line, segment_index, pole_index + 1)        

    def _create_pole(self, line, segment_index):
        pole = Pole(
            id=self.ids.next("P"),
            name="Pole",
            pole_number=self.ids.next("JP"),
            material="Concrete",
            height_m=12,
            installation_year=2021
        )
        # line.terminal_pole = pole
        line.poles.append(pole)
        self.network.poles.append(pole)
        # self._create_switch(pole)
        # pole_index = len(self.poles)
        if segment_index % rules.SECTION_SWITCH_INTERVAL == 0:
            self._create_switch(pole)
        # self._create_transformer(pole)
        if segment_index % rules.TRANSFORMER_INTERVAL == 0:
            self._create_transformer(pole)

    def _create_switch(self, pole):
        switch = Switch(
            id=self.ids.next("SW"),
            name="Load Break Switch",
            switch_type="Load Break Switch",
            status="CLOSED",
            normally_closed=True,
            voltage_kV=(self.config.feeder_voltage_kv),
            mounted_on=pole
        )
        pole.mounted_assets.append(switch)
        self.network.switches.append(switch)
    
    def _create_transformer(self, pole):
        transformer = Transformer(
            id=self.ids.next("TR"),
            name="Distribution Transformer",
            rating_kVA=300,
            primary_voltage=11,
            secondary_voltage=0.415,
            vector_group="Dyn11",
            cooling="ONAN",
            mounted_on=pole
        )
        pole.mounted_assets.append(transformer)
        self.network.transformers.append(transformer)

        count = random.randint(
            rules.MIN_CUSTOMERS,
            rules.MAX_CUSTOMERS
        )
        for _ in range(count):
            self._create_customer(transformer)

    def _create_customer(self, transformer):
        customer_type = random.choice(list(rules.CUSTOMER_LOADS.keys()))
        low, high = rules.CUSTOMER_LOADS[customer_type]
        load = round(random.uniform(low, high), 2)
        customer = Customer(
            id=self.ids.next("C", width=4),
            name="Customer",
            customer_type=customer_type,
            load_kW=load,
            transformer=transformer
        )
        transformer.customers.append(customer)
        self.network.customers.append(customer)