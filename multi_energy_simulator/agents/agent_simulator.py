import mosaik_api
from .community_agent import CommunityAgent
from .coordinator_agent import CoordinatorAgent

META = {
    'type': 'time-based',
    'models': {
        'Agent': {
            'public': True,
            'params': [],
            'attrs': ['decision'],
        },
    },
}

class AgentSimulator(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.entities = {}

    def create(self, num, model, **model_params):
        entities = []
        for _ in range(num):
            eid = f'agent_{len(self.entities)+1}'
            self.entities[eid] = {
                'agent': None,
                'decision': None,
            }
            entities.append({'eid': eid, 'type': model})
        return entities

    def step(self, time, inputs, max_advance):
        for eid, entity in self.entities.items():
            agent = entity.get('agent')
            if agent:
                entity['decision'] = agent
        return time + max_advance

