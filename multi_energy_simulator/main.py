import mosaik
from .config.scenario_config import DURATION, TIME_STEP
from .config.community_config import COMMUNITIES

SIM_CONFIG = {
    'PVSim': {'python': 'multi_energy_simulator.models.pv_model:PVSimulator'},
    'BatterySim': {'python': 'multi_energy_simulator.models.battery_model:BatterySimulator'},
    'HeatPumpSim': {'python': 'multi_energy_simulator.models.heatpump_model:HeatPumpSimulator'},
    'GridSim': {'python': 'multi_energy_simulator.models.grid_model:GridSimulator'},
    'AgentSim': {'python': 'multi_energy_simulator.agents.agent_simulator:AgentSimulator'},
}

def create_communities(world, pv_sim, battery_sim, heatpump_sim):
    communities = {}
    for cid, cfg in COMMUNITIES.items():
        pv_entities = [pv_sim.PVSystem(**p) for p in cfg.get('pv_systems', [])]
        batt_entities = [battery_sim.Battery(**b) for b in cfg.get('batteries', [])]
        hp_entities = [heatpump_sim.HeatPump(**hp) for hp in cfg.get('heat_pumps', [])]
        communities[cid] = {
            'pv': pv_entities,
            'batteries': batt_entities,
            'heat_pumps': hp_entities,
        }
    return communities

def establish_connections(world, communities, grid):
    # Minimal connections: PV -> Grid
    for cid, comps in communities.items():
        for pv in comps['pv']:
            world.connect(pv, grid, ('p_out', 'exchange'))


def create_agents(world, agent_sim, communities):
    # Placeholder for agent creation
    agents = []
    for cid, comps in communities.items():
        agent = agent_sim.Agent()
        agents.append(agent)
    return agents


def run_simulation(duration=DURATION):
    world = mosaik.World(SIM_CONFIG)
    pv_sim = world.start('PVSim')
    battery_sim = world.start('BatterySim')
    heatpump_sim = world.start('HeatPumpSim')
    grid_sim = world.start('GridSim')
    agent_sim = world.start('AgentSim')

    communities = create_communities(world, pv_sim, battery_sim, heatpump_sim)
    grid = grid_sim.Grid(topology='multi_energy_simulator/data/grid_topology.json')
    establish_connections(world, communities, grid)
    create_agents(world, agent_sim, communities)

    world.run(until=duration)
    return world

if __name__ == '__main__':
    run_simulation()
