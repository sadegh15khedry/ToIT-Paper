import sys
import os
import time
import numpy as np
from report import save_report
from reinforcement_learning_agent import ReinforcementLearningAgent
from vehicle_movement import vehicle_movement_function
from task_management import manage_tasks, generate_tasks
from initialization import load_config, initialize_edge_servers, initialize_vehicles, load_mobility_csv

class Simulation:
    def __init__(self, algorithm, time_step_length, max_iterations, mobility_file_path, mode, edge_file_path, vehicle_file_path, report_path):
        self.mode = mode
        self.edge_servers = initialize_edge_servers(edge_file_path)
        self.vehicles = initialize_vehicles(vehicle_file_path)
        self.start_time = 0
        self.finish_time = 0
        self.algorithm = algorithm
        self.iteration_count = 1
        self.time_step_length = time_step_length
        self.max_iterations = max_iterations
        self.report_path = report_path
        self.mobility_file = load_mobility_csv(mobility_file_path)
        
    
    def save_q_table(self, q_table):
        np.save('../results/q_table/q_table.npy', q_table)
        # print (type(q_table))
        
    def load_q_table(self):
        q_table = np.load('../results/q_table/q_table.npy')
        print(ReinforcementLearningAgent.q_table)
        print("-------------------")
        # print(q_table)
        ReinforcementLearningAgent.q_table = q_table
        print(ReinforcementLearningAgent.q_table)
        
    # def initialize_vehicles(self):
    def run(self):
        if self.mode == 'test' or self.mode == "test_with_q_table_update":
            self.load_q_table()
        print("Running simulation stated!")
        self.start_time = time.time()
        should_update_q_table = True
        
        if(self.mode == 'test'):
            should_update_q_table = False
        
        ReinforcementLearningAgent.should_update_q_table = should_update_q_table
        
        while self.iteration_count <= self.max_iterations:
            # iteration_start_time = time.time()
            print(f"Iteration: {self.iteration_count} started  ----------------------------------------------------------------")
            
            # if(self.iteration_count % 3 == 1):
            generate_tasks(self.vehicles, self.iteration_count)
            vehicle_movement_function(self.vehicles, self.iteration_count, self.mobility_file)
            manage_tasks(self.vehicles, self.edge_servers, self.iteration_count, self.algorithm)

            
            print(f"Iteration: {self.iteration_count} ended ----------------------------------------------------------------")
            self.iteration_count += 1



        # self.finish_time = time.time()
        print(f"Simulation finished! Total iterations: {self.iteration_count}.")
        save_report(self.vehicles, self.report_path)
        if(self.mode == 'train'):
            print(self.vehicles[0].agent.q_table)
            self.save_q_table(self.vehicles[0].agent.q_table)
