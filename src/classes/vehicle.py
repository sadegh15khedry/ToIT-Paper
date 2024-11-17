import pandas as pd
import random
from reinforcement_learning_agent import ReinforcementLearningAgent
from task import Task
class Vehicle:
    def __init__(self, id, x, y, speed, direction, frequency):
        self.id = id
        self.x = x
        self.y = y
        self.frequency = frequency
        self.new_task_id = 0
        self.speed = speed
        self.direction = direction
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
        # print("Vehicle id:",self.id,"  Task size:",size,"  Task cycle", cycle)
        
        size *= 10**6
        cycle *= 10**9
        
            
        task = Task(self.get_new_task_id(), self, time, cycle, size)
        self.undecided_tasks.append(task)
        # task.print_task_info()
        # print(f"task:{task.id} is genenrated in the vehicle:{self.id}")
        
    def handle_task_finish(self, task, time):
        print(f"-------------------------finish---------------task:{task.id}, energy:{task.energy}, response time: {task.response_time} location: {task.execution_location}")
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
            # print(f"task:{task.id} is finished processing on vehicle:{self.id}")
            
            return False
        return True
         
    def run_new_task(self, time):
        if self.local_execution_queue and self.running_task is None:
            task = self.local_execution_queue.pop(0)
            task.start_time = time
            self.running_task = task
            # print(f"task:{task.id} is now processing on vehicle:{self.id}")
            
    
    # def print_vehicle_info(self):
    #     print(f"id: {self.id}, x: {self.x}, y: {self.y}, speed: {self.speed}, direction: {self.direction}")
    #     print(f"undecided tasks count: {len(self.undecided_tasks)}")
    
        
    def find_closest_edge_server(self, edge_servers):
        """
        Finds and returns the closest edge server to the vehicle based on Euclidean distance.

        Parameters:
        - edge_servers (list): A list of edge server objects. Each server should have 'x' and 'y' attributes.

        Returns:
        - closest_server: The edge server object closest to the vehicle.
        """
        min_distance = float('inf')  # Initialize with infinity
        closest_server = None        # Placeholder for the closest server

        for server in edge_servers:
            # Extract 'x' and 'y' coordinates from the server
            # Ensure they are scalar values, not Pandas Series or other iterable types

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

            # Ensure vehicle's 'x' and 'y' are scalars
            if isinstance(self.x, pd.Series):
                if self.x.empty:
                    raise ValueError(f"Vehicle {self.id} has an empty 'x' value.")
                elif self.x.size == 1:
                    vehicle_x = self.x.item()
                else:
                    raise ValueError(f"Vehicle {self.id} has multiple 'x' values: {self.x}")
            else:
                vehicle_x = self.x

            if isinstance(self.y, pd.Series):
                if self.y.empty:
                    raise ValueError(f"Vehicle {self.id} has an empty 'y' value.")
                elif self.y.size == 1:
                    vehicle_y = self.y.item()
                else:
                    raise ValueError(f"Vehicle {self.id} has multiple 'y' values: {self.y}")
            else:
                vehicle_y = self.y

            # Calculate Euclidean distance
            distance = ((server_x - vehicle_x)**2 + (server_y - vehicle_y)**2)**0.5

            # Debugging Statements (Optional)
            # Uncomment the following lines if you need to trace the values
            # print(f"Vehicle ({vehicle_x}, {vehicle_y}) to Server {server.id} ({server_x}, {server_y}) Distance: {distance}")

            # Update the closest server if a closer one is found
            if distance < min_distance:
                min_distance = distance
                closest_server = server

        return closest_server , min_distance


        
    

