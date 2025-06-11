import mosaik_api

META = {
    'type': 'time-based',
    'models': {
        'HeatPump': {
            'public': True,
            'params': ['rated_power', 'cop_heating', 'cop_cooling'],
            'attrs': ['p_el', 'q_th', 'mode', 'outdoor_temp'],
        },
    },
}

class HeatPumpSimulator(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.entities = {}

    def create(self, num, model, **model_params):
        entities = []
        for _ in range(num):
            eid = f'hp_{len(self.entities)+1}'
            self.entities[eid] = {
                'rated_power': model_params.get('rated_power', 10.0),
                'cop_heating': model_params.get('cop_heating', 3.0),
                'cop_cooling': model_params.get('cop_cooling', 3.0),
                'p_el': 0.0,
                'q_th': 0.0,
                'mode': 'heating',
            }
            entities.append({'eid': eid, 'type': model})
        return entities

    def step(self, time, inputs, max_advance):
        for eid, entity in self.entities.items():
            mode = inputs.get(eid, {}).get('mode', {0: 'heating'}).get(time, 'heating')
            outdoor_temp = inputs.get(eid, {}).get('outdoor_temp', {0: 15}).get(time, 15)
            entity['mode'] = mode
            if mode == 'heating':
                cop = entity['cop_heating']
            else:
                cop = entity['cop_cooling']
            entity['p_el'] = entity['rated_power']
            entity['q_th'] = entity['p_el'] * cop
        return time + max_advance

    def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            ent = self.entities[eid]
            data[eid] = {attr: ent.get(attr) for attr in attrs}
        return data

