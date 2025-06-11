# Example community definitions
COMMUNITIES = {
    'residential_1': {
        'pv_systems': [
            {'rated_power': 5.0, 'tilt': 30, 'azimuth': 180},
            {'rated_power': 7.5, 'tilt': 30, 'azimuth': 180},
        ],
        'batteries': [
            {'capacity': 13.5, 'max_power': 5.0, 'efficiency': 0.95},
        ],
        'heat_pumps': [
            {'rated_power': 12.0, 'cop_heating': 3.5, 'cop_cooling': 4.0},
            {'rated_power': 8.0, 'cop_heating': 3.2, 'cop_cooling': 3.8},
        ],
        'location': {'lat': 52.5, 'lon': 13.4},
    },
    'commercial_1': {
        'pv_systems': [
            {'rated_power': 100.0, 'tilt': 15, 'azimuth': 180},
        ],
        'batteries': [
            {'capacity': 250.0, 'max_power': 50.0, 'efficiency': 0.93},
        ],
        'heat_pumps': [
            {'rated_power': 150.0, 'cop_heating': 3.8, 'cop_cooling': 4.2},
        ],
        'location': {'lat': 52.6, 'lon': 13.5},
    },
}
