import mosaik_api

META = {
    'type': 'time-based',
    'models': {
        'Battery': {
            'public': True,
            'params': ['capacity', 'max_power', 'efficiency'],
            'attrs': ['soc', 'p_charge', 'p_discharge', 'available_capacity'],
        },
    },
}

class BatterySimulator(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.entities = {}

    def create(self, num, model, **model_params):
        entities = []
        for _ in range(num):
            eid = f'batt_{len(self.entities)+1}'
            self.entities[eid] = {
                'capacity': model_params.get('capacity', 10.0),
                'max_power': model_params.get('max_power', 5.0),
                'efficiency': model_params.get('efficiency', 0.95),
                'soc': model_params.get('capacity', 10.0) / 2,
            }
            entities.append({'eid': eid, 'type': model})
        return entities

    def step(self, time, inputs, max_advance):
        for eid, entity in self.entities.items():
            p_in = inputs.get(eid, {}).get('p_charge', {0: 0}).get(time, 0)
            p_out = inputs.get(eid, {}).get('p_discharge', {0: 0}).get(time, 0)
            delta = (p_in * entity['efficiency'] - p_out / entity['efficiency']) * (max_advance / 3600.0)
            entity['soc'] = max(0.0, min(entity['capacity'], entity['soc'] + delta))
            entity['available_capacity'] = entity['capacity'] - entity['soc']
        return time + max_advance

    def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            ent = self.entities[eid]
            data[eid] = {attr: ent.get(attr) for attr in attrs}
        return data

