import pandas as pd
import random
from reinforcement_learning_agent import ReinforcementLearningAgent
from task import Task
class Device:
    def __init__(self, id, x, y, frequency):
        self.id = id
        self.x = x
        self.y = y
        self.frequency = frequency
        self.new_task_id = 0
        self.transmission_power = 300*(10**-3)
        self.running_task = None
        self.local_execution_queue = []
        self.unfinished_offload_tasks = []
        self.undecided_tasks = []
        self.finished_tasks = []
        self.agent = ReinforcementLearningAgent(self)
       
        
 
    def generate_task(self, time):
        size = random.randint(2,10)
        cycle = random.randint(2,10)
        
        size *= 10**6
        cycle *= 10**9
        
            
        task = Task(self.get_new_task_id(), self, time, cycle, size)
        self.undecided_tasks.append(task)

        
    def handle_task_finish(self, task, time):

        task.end_time = time
        self.finished_tasks.append(task)
        self.agent.check_if_need_to_update_q_table()
        
        if task.execution_location == 0:
            self.running_task = None
        elif task.execution_location == 1:
            self.unfinished_offload_tasks.remove(task)
            
        
    def get_new_task_id(self):
        self.new_task_id += 1
        return self.new_task_id
    
    def is_busy(self, time):
        task = self.running_task
        if task == None:
            return False
        
        is_finished = task.is_finished(time)
        if is_finished:
            self.handle_task_finish(task, time)
            
            return False
        return True
         
    def run_new_task(self, time):
        if self.local_execution_queue and self.running_task is None:
            task = self.local_execution_queue.pop(0)
            task.start_time = time
            self.running_task = task
    
        
    def find_closest_edge_server(self, edge_servers):

        min_distance = float('inf')  # Initialize with infinity
        closest_server = None        # Placeholder for the closest server

        for server in edge_servers:

            # Handle server.x
            if isinstance(server.x, pd.Series):
                if server.x.empty:
                    raise ValueError(f"Server {server.id} has an empty 'x' value.")
                elif server.x.size == 1:
                    server_x = server.x.item()
                else:
                    raise ValueError(f"Server {server.id} has multiple 'x' values: {server.x}")
            else:
                server_x = server.x

            # Handle server.y
            if isinstance(server.y, pd.Series):
                if server.y.empty:
                    raise ValueError(f"Server {server.id} has an empty 'y' value.")
                elif server.y.size == 1:
                    server_y = server.y.item()
                else:
                    raise ValueError(f"Server {server.id} has multiple 'y' values: {server.y}")
            else:
                server_y = server.y

            # Ensure device's 'x' and 'y' are scalars
            if isinstance(self.x, pd.Series):
                if self.x.empty:
                    raise ValueError(f"Device {self.id} has an empty 'x' value.")
                elif self.x.size == 1:
                    device_x = self.x.item()
                else:
                    raise ValueError(f"Device {self.id} has multiple 'x' values: {self.x}")
            else:
                device_x = self.x

            if isinstance(self.y, pd.Series):
                if self.y.empty:
                    raise ValueError(f"Device {self.id} has an empty 'y' value.")
                elif self.y.size == 1:
                    device_y = self.y.item()
                else:
                    raise ValueError(f"Device {self.id} has multiple 'y' values: {self.y}")
            else:
                device_y = self.y

            # Calculate Euclidean distance
            distance = ((server_x - device_x)**2 + (server_y - device_y)**2)**0.5


            # Update the closest server if a closer one is found
            if distance < min_distance:
                min_distance = distance
                closest_server = server

        return closest_server , min_distance


        
    

