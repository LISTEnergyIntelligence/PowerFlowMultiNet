import mosaik_api
import json
import networkx as nx

META = {
    'type': 'time-based',
    'models': {
        'Grid': {
            'public': True,
            'params': ['topology'],
            'attrs': ['exchange'],
        },
    },
}

class GridSimulator(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.entities = {}

    def create(self, num, model, **model_params):
        entities = []
        for _ in range(num):
            eid = f'grid_{len(self.entities)+1}'
            topology_file = model_params.get('topology')
            if topology_file:
                with open(topology_file) as f:
                    data = json.load(f)
                graph = nx.node_link_graph(data)
            else:
                graph = nx.Graph()
            self.entities[eid] = {'graph': graph, 'exchange': 0.0}
            entities.append({'eid': eid, 'type': model})
        return entities

    def step(self, time, inputs, max_advance):
        # For simplicity, just sum exchanges
        for eid, entity in self.entities.items():
            exchange = inputs.get(eid, {}).get('exchange', {0: 0}).get(time, 0)
            entity['exchange'] = exchange
        return time + max_advance

    def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            ent = self.entities[eid]
            data[eid] = {attr: ent.get(attr) for attr in attrs}
        return data

