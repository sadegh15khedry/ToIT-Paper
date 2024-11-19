import sys
import os
import time
import numpy as np
import pandas as pd
from report import save_report
from reinforcement_learning_agent import ReinforcementLearningAgent
from task_management import manage_tasks, generate_tasks
from initialization import load_config, initialize_edge_servers, initialize_devices

class Simulation:
    def __init__(self, algorithm, time_step_length, max_iterations, mode, edge_file_path, device_file_path, report_path, q_table_path):
        self.mode = mode
        self.edge_servers = initialize_edge_servers(edge_file_path)
        self.devices = initialize_devices(device_file_path)
        self.start_time = 0
        self.finish_time = 0
        self.algorithm = algorithm
        self.q_table_path = q_table_path
        self.iteration_count = 1
        self.time_step_length = time_step_length
        self.max_iterations = max_iterations
        self.report_path = report_path
        
    
    def save_q_table(self, q_table):
        np.save(self.q_table_path+'.npy', q_table)
        # np.savetxt(self.q_table_path+'.txt', q_table, fmt="%d")
        # print (type(q_table))
        
        
    def load_q_table(self):
        q_table = np.load('../results/q_table/q_table.npy')
        print(ReinforcementLearningAgent.q_table)
        print("-------------------")
        # print(q_table)
        ReinforcementLearningAgent.q_table = q_table
        print(ReinforcementLearningAgent.q_table)
        

    def run(self):
        if self.mode == 'test' or self.mode == "test_with_q_table_update":
            self.load_q_table()
        # print("Running simulation stated!")
        self.start_time = time.time()
        should_update_q_table = True
        
        if(self.mode == 'test'):
            should_update_q_table = False
        
        ReinforcementLearningAgent.should_update_q_table = should_update_q_table
        
        while self.iteration_count <= self.max_iterations:
            # iteration_start_time = time.time()
            print(f"Iteration: {self.iteration_count}")
            
            if(self.iteration_count % 100 == 1):
                generate_tasks(self.devices, self.iteration_count)
            manage_tasks(self.devices, self.edge_servers, self.iteration_count, self.algorithm)

            
            # print(f"Iteration: {self.iteration_count} ended ----------------------------------------------------------------")
            self.iteration_count += 1



        # self.finish_time = time.time()
        print(f"Simulation finished! Total iterations: {self.iteration_count}.")
        save_report(self.devices, self.report_path)
        if(self.mode == 'train'):
            print(self.devices[0].agent.q_table)
            self.save_q_table(self.devices[0].agent.q_table)
