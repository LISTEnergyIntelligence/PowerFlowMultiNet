import mosaik_api

META = {
    'type': 'time-based',
    'models': {
        'PVSystem': {
            'public': True,
            'params': ['rated_power', 'efficiency', 'tilt', 'azimuth'],
            'attrs': ['p_out', 'irradiance', 'temperature'],
        },
    },
}

class PVSimulator(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.entities = {}

    def create(self, num, model, **model_params):
        entities = []
        for i in range(num):
            eid = f'pv_{len(self.entities)+1}'
            self.entities[eid] = {
                'rated_power': model_params.get('rated_power', 1.0),
                'efficiency': model_params.get('efficiency', 0.9),
                'p_out': 0.0,
            }
            entities.append({'eid': eid, 'type': model})
        return entities

    def step(self, time, inputs, max_advance):
        for eid, entity in self.entities.items():
            irr = inputs.get(eid, {}).get('irradiance', {0: 0}).get(time, 0)
            temp = inputs.get(eid, {}).get('temperature', {0: 25}).get(time, 25)
            entity['p_out'] = entity['rated_power'] * entity['efficiency'] * irr
        return time + max_advance

    def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            ent = self.entities[eid]
            data[eid] = {attr: ent.get(attr) for attr in attrs}
        return data

