import sys
import os
import time

from vehicle import Vehicle
from edge_server import EdgeServer
from fog_server import FogServer
from core import Core
from cloud_server import CloudServer
from vehicle_movement import load_mobility_csv, vehicle_movement_funciton
from application_generation import vehicles_applicaton_generation
from task_management import manage_tasks
import json

class Simulation:
    def __init__(self, config_file, algorithm, time_step, max_iterations, mobility_file_path):
        self.config = self.load_config(config_file)
        self.edge_servers = self.initialize_edge_servers()
        self.fog_servers = self.initialize_fog_servers()
        self.cloud_servers = self.initialize_cloud_servers()
        self.vehicles = self.initialize_vehicles()
        self.start_time = 0
        self.finish_time = 0
        self.algorithm = algorithm
        self.iteration_count = 0
        self.time_step = time_step
        self.max_iterations = max_iterations
        self.mobilty_file = load_mobility_csv(mobility_file_path)
        
        
    def load_config(self, config_file):
        with open(config_file) as file:
            return json.load(file)
        
    def get_cores(self, config):
        cores = []
        for core in config['cores']:
            cores.append(Core(core['id'], core['frequency'], core['voltage']))
        return cores
    
    def initialize_edge_servers(self):
        edge_servers = []
        for edge_server_config in self.config['edge_servers']:
            cores = self.get_cores(edge_server_config)
            
            edge_server = EdgeServer(edge_server_config['id'], cores, edge_server_config['x'],
                                     edge_server_config['y'], edge_server_config['memory'],
                                     edge_server_config['bandwidth'])
            
            print(f"Edge Server id: {edge_server.id} core count: {len(edge_server.cores)} x: {edge_server.x} y: {edge_server.y} memory: {edge_server.memory} bandwidth: {edge_server.bandwidth}")

            edge_servers.append(edge_server)
        print(f"Initialized {len(edge_servers)} edge servers.")
        return edge_servers
    
    def initialize_cloud_servers(self):
        cloud_servers = []
        for cloud_server_config in self.config['cloud_servers']:
            cores = self.get_cores(cloud_server_config)
            
            cloud_server = CloudServer(cloud_server_config['id'], cores, cloud_server_config['x'],
                                     cloud_server_config['y'], cloud_server_config['memory'],
                                     cloud_server_config['bandwidth'])
            
            print(f"Cloud server id: {cloud_server.id} core count: {len(cloud_server.cores)} x: {cloud_server.x} y: {cloud_server.y} memory: {cloud_server.memory} bandwidth: {cloud_server.bandwidth}")
            cloud_servers.append(cloud_server)
            
        print(f"Initialized {len(cloud_servers)} cloud servers.")
        return cloud_servers
    
    def initialize_fog_servers(self):
        fog_servers = []
        for fog_server_config in self.config['fog_servers']:
            cores = self.get_cores(fog_server_config)
            
            fog_server = CloudServer(fog_server_config['id'], cores, fog_server_config['x'],
                                     fog_server_config['y'], fog_server_config['memory'],
                                     fog_server_config['bandwidth'])
            
            print(f"Fog server id: {fog_server.id} core count: {len(fog_server.cores)} x: {fog_server.x} y: {fog_server.y} memory: {fog_server.memory} bandwidth: {fog_server.bandwidth}")
            fog_servers.append(fog_server)
            
        print(f"Initialized {len(fog_servers)} fog servers.")
        return fog_servers
    
    def initialize_vehicles(self):
        vehicles = []
        for vehicle_config in self.config['vehicles']:
            cores = self.get_cores(vehicle_config)
            vehicle = Vehicle(vehicle_config['id'], vehicle_config['x'], vehicle_config['y'],
                                    vehicle_config['speed'], vehicle_config['direction'], cores, vehicle_config['memory'], vehicle_config['bandwidth'])
            print(f"vehicle id: {vehicle.id} core count: {len(vehicle.cores)} x: {vehicle.x} y: {vehicle.y} speed: {vehicle.speed}, direction: {vehicle.direction} memory: {vehicle.memory} bandwidth: {vehicle.bandwidth}")
            vehicles.append(vehicle)

        print(f"Initialized {len(vehicles)} vehicles.")
        return vehicles
    
    # def initialize_vehicles(self):
    def run(self):
        print("Running simulation stated!")
        self.start_time = time.time()

        while self.iteration_count <= self.max_iterations:
            iteration_start_time = time.time()
            self.iteration_count += 1
            print(f"Iteration: {self.iteration_count} started at {iteration_start_time} ----------------------------------------------------------------")
            
            vehicles_applicaton_generation(self.vehicles)
            vehicle_movement_funciton(self.vehicles, self.iteration_count, self.mobilty_file)
            manage_tasks(self.vehicles, self.edge_servers, self.iteration_count)
            
            time.sleep(self.time_step)
            print(f"Iteration: {self.iteration_count} started at {iteration_start_time} ----------------------------------------------------------------")

        self.finish_time = time.time()
        print(f"Simulation finished! Total execution time: {self.finish_time - self.start_time} seconds.")
