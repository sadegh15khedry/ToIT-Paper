class Application:
    def __init__(self, id, vehicle_id, deadline, criticality, start_task, edges):
        self.id = id
        self.vehicle_id = vehicle_id
        self.deadline = deadline
        self.criticality = criticality
        self.start_task = start_task
        self.edges = edges
        self.start_time = None
        self.finish_time = None
        self.response_time = None
        self.unfinished_tasks = []
        self.finished_tasks = []
        
        
    def set_finish_time(self, end_time):
        self.finish_time = end_time
        
    def set_start_time(self, start_time):
        self.start_time = start_time
        
    def print_application_info(self):
        print(f"Application ID: {self.id}, Vehicle ID: {self.vehicle_id}, Deadline: {self.deadline}, Criticality: {self.criticality},  Start Task: {self.start_task}, Start Time: {self.start_time}, Finish Time: {self.finish_time}, Response Time: {self.response_time}")
        

        
    