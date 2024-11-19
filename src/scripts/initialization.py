from device import Device
from edge_server import EdgeServer
import json
import pandas as pd
from core import Core

def load_config(config_file):
    with open(config_file) as file:
        return json.load(file)

def get_cores(cores_config):
    cores = []
    for core in cores_config:
        core_id = core['id']
        core_frequency = core['frequency']
        cores.append(Core(core_id, core_frequency))
    return cores
        
        
def initialize_edge_servers(edge_server_file):
    config = load_config(edge_server_file)
    edge_servers = []
    for edge_server_config in config['edge_servers']:
        cores = get_cores(edge_server_config['cores'])
        edge_server = EdgeServer(edge_server_config['id'], cores, edge_server_config['x'],
                                     edge_server_config['y'], edge_server_config['bandwidth'])
            
        print(f"Edge Server id: {edge_server.id}, x: {edge_server.x} y: {edge_server.y} core_count: {len(edge_server.cores)}")

        edge_servers.append(edge_server)
    print(f"Initialized {len(edge_servers)} edge servers.")
    return edge_servers
    

    
def initialize_devices(device_file_path):
    devices_config = load_config(device_file_path)
    devices = []
    for device_config in devices_config['devices']:
        cores = get_cores(device_config['cores'])
        device = Device(device_config['id'], cores, device_config['x'], device_config['y'], device_config['frequency'])
        print(f"device id: {device.id} x: {device.x} y: {device.y}, core_count: {len(device.cores)}")
        devices.append(device)

        print(f"Initialized {len(devices)} devices.")
    return devices