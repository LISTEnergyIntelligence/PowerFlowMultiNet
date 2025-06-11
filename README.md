# Multi-Energy Simulator

This repository contains a minimal multi-energy simulator implementation based on the Mosaik 3.x framework. It models photovoltaic systems, battery storage, heat pumps, and a simple grid. Example community configurations and data are included.

## Requirements

- Python 3.8+
- `mosaik`, `mosaik-api`, `numpy`, `pandas`, `matplotlib`, `networkx`

Install dependencies via pip:

```bash
pip install mosaik mosaik-api numpy pandas matplotlib networkx
```

## Running the Example

Execute a short example simulation:

```bash
python run_example.py
```

The script runs a one-hour simulation with sample communities defined in `multi_energy_simulator/config/community_config.py`.
