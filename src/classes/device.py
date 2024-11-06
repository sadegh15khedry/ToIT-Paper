from reinforcement_learning_agent import ReinforcementLearnigAgent
from task import Task
class Device:
    def __init__(self, id, x, y, speed, direction, frequency):
        self.id = id
        self.x = x
        self.y = y
        self.frequency = frequency
        self.new_task_id = 0
        self.speed = speed
        self.direction = direction
        self.transmission_power = 100*(10**-3)
        self.runnig_task = None
        self.local_execution_queue = []
        self.unfinished_offload_tasks = []
        self.undecided_tasks = []
        self.finished_tasks = []
        self.agent = ReinforcementLearnigAgent(self)
        self.last_task_type = 0
        
 
    def generate_task(self, time):
        if self.last_task_type % 9 == 0:
            size = 2000000
            cycle = 2000000
        elif self.last_task_type % 9 == 1:
            size = 5000000
            cycle = 5000000
        elif self.last_task_type % 9 == 2:
            size = 7000000
            cycle = 7000000
        elif self.last_task_type % 9 == 3:
            size = 2000000
            cycle = 2000000
        elif self.last_task_type % 9 == 4:
            size = 5000000
            cycle = 5000000
        elif self.last_task_type % 9 == 5:
            size = 7000000
            cycle = 7000000
        elif self.last_task_type % 9 == 6:
            size = 2000000
            cycle = 2000000
        elif self.last_task_type % 9 == 7:
            size = 5000000
            cycle = 5000000
        elif self.last_task_type % 9 == 8:
            size = 7000000
            cycle = 7000000
            
        task = Task(self.get_new_task_id(), self, time, cycle, size)
        self.undecided_tasks.append(task)
        # task.print_task_info()
        self.last_task_type += 1
        # print(f"task:{task.id} is genenrated in the vehicle:{self.id}")
        
    def handle_task_finish(self, task, time):
        task.end_time = time
        self.finished_tasks.append(task)
        self.agent.check_if_need_to_update_q_table()
        
        if task.execution_location == 0:
            self.runnig_task = None
        elif task.execution_location == 1:
            self.unfinished_offload_tasks.remove(task)
            
        
    def get_new_task_id(self):
        self.new_task_id += 1
        return self.new_task_id
    
    def is_busy(self, time):
        task = self.runnig_task
        if task == None:
            return False
        
        is_finished = task.is_finished(time)
        if is_finished:
            self.handle_task_finish(task, time)
            # print(f"task:{task.id} is finished processing on vehicle:{self.id}")
            
            return False
        return True
         
    def run_new_task(self, time):
        if self.local_execution_queue and self.runnig_task is None:
            task = self.local_execution_queue.pop(0)
            task.start_time = time
            self.runnig_task = task
            # print(f"task:{task.id} is now processing on vehicle:{self.id}")
            
    
    # def print_vehicle_info(self):
    #     print(f"id: {self.id}, x: {self.x}, y: {self.y}, speed: {self.speed}, direction: {self.direction}")
    #     print(f"undecided tasks count: {len(self.undecided_tasks)}")
    
        
    def find_closest_edge_server(self, edge_servers):
        min_distance = float('inf')
        closest_server = None
        for server in edge_servers:
            distance = ((server.x - self.x)**2 + (server.y - self.y)**2)**0.5
            if distance < min_distance:
                min_distance = distance
                closest_server = server
        return closest_server
        
    

