from device import Device
from edge_server import EdgeServer
import json
import pandas as pd


def load_config(config_file):
    with open(config_file) as file:
        return json.load(file)

    
def initialize_edge_servers(edge_server_file):
    config = load_config(edge_server_file)
    edge_servers = []
    for edge_server_config in config['edge_servers']:
        edge_server = EdgeServer(edge_server_config['id'], edge_server_config['x'],
                                     edge_server_config['y'],edge_server_config['frequency'], edge_server_config['bandwidth'])
            
        print(f"Edge Server id: {edge_server.id}, x: {edge_server.x} y: {edge_server.y}")

        edge_servers.append(edge_server)
    print(f"Initialized {len(edge_servers)} edge servers.")
    return edge_servers
    

    
def initialize_devices(device_file_path):
    config = load_config(device_file_path)
    devices = []
    for device_config in config['devices']:
        device = Device(device_config['id'], device_config['x'], device_config['y'],
                                device_config['frequency'])
        print(f"device id: {device.id} x: {device.x} y: {device.y}")
        devices.append(device)

        print(f"Initialized {len(devices)} devices.")
    return devices
    
def load_mobility_csv(path):
    file = pd.read_csv(path)
    return file