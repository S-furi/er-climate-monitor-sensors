#!/usr/bin/env python3

import yaml
import random
import os

selected_sensors = {
    "idro_level": [
        "Diga di Ridracoli",
        "Castelbolognese",
        "Ponte degli Alpini",
        "S. Carlo",
        "Ponte Nibbiano Tidoncello"
    ],
    "temp": [
        "Sestola",
        "Cesenatico porto",
        "Piacenza urbana",
        "Cesena urbana",
        "S. Marino",
        "Bologna San Luca",
        "Lavezzola"
    ],
    "humidity": [
        "Carpineta",
        "Cesena urbana",
        "Reggio nell'Emilia urbana",
        "Novafeltria",
        "Mirabello",
        "Rimini urbana",
        "Piacenza urbana"
    ],
    "wind": [
        "Bologna urbana",
        "Reggio nell'Emilia urbana",
        "GIRALDA",
        "S. Pietro Capofiume",
        "Martorano",
        "Madonna dei Fornelli",
        "Modena urbana",
        "Bologna Torre Asinelli"
    ],
    "rain": [
        "S. Felice sul Panaro",
        "Madonna dei Fornelli",
        "Bologna San Luca",
        "Paderno",
        "Secondo Salto",
        "Castel San Pietro Arpa",
        "S. Cassiano sul Lamone",
        "Premilcuore",
        "Castrocaro",
        "S. Maria Nova"
    ]
}

def generate_sensor_config(name: str, sensor_type: str, port: int, ip: str) -> dict:
    queries = ["soglia1", "soglia2", "soglia3"] if sensor_type != 'rain' else []
    return {
        "sensor": {
            "information": {
                "name": name,
                "description": "General Sensor Description",
                "type": sensor_type,
                "queries": queries,
            },
            "ethernet": {
                "port": port,
                "ip": ip
            },
            "registry": {
                "url": "http://127.0.0.1:3000/v0/api/sensor",
                "registerPath": "/register",
                "shutDownPath": "/shutdown",
                "key": "secretKey"
            },
            "apiGateway": {
                "url": "localhost",
                "port": 3000
            },
            "cronjob": {
                "day_of_week": "0-6",
                "hour": "*",
                "minute": "*"
            }
        }
    }

if __name__ == "__main__":
    directory = 'sensors_config'
    os.makedirs(directory, exist_ok=True)

    num_sensors = sum(map(lambda x: len(x), selected_sensors.values()))
    print(num_sensors)
    ips = [ f'192.168.101.{n}' for n in random.sample(range(1, 255), num_sensors) ]
    ports = random.sample(range(12000, 20000), num_sensors)

    i = 0
    for sensor_type, sensor_names in selected_sensors.items():
        for sensor_name in sensor_names:
            sensor_name = sensor_name.replace(' ', '')
            config = generate_sensor_config(sensor_name, sensor_type, ports[i], ips[i])
            output_file = os.path.join(directory, f'sensor_{sensor_type}_{sensor_name}.yaml')
            with open(output_file, 'w') as f:
                yaml.safe_dump(config, f, default_flow_style=False, sort_keys=False)
            i += 1
