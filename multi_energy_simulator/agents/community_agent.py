class CommunityAgent:
    def __init__(self, community_id, components):
        self.community_id = community_id
        self.pv_systems = components.get('pv', [])
        self.batteries = components.get('batteries', [])
        self.heat_pumps = components.get('heat_pumps', [])

    def optimize_energy_flow(self, forecast):
        pass

    def participate_in_market(self, prices):
        pass

