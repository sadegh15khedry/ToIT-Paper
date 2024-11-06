import time

class Core:
    def __init__(self, id, frequency, voltage):
        self.id = id
        self.frequency = frequency
        self.voltage = voltage
        self.runnig_task = None
        self.task_queue = []
        self.running_task = None
        
    def run_task(self, task):
        self.task_queue.remove(task)
        self.running_task = task
        task.start_time = time.time()
        task.end_time = task.start_time + task.execution_time
        self.running_task = None
        
        
    def add_task_to_queue(self, task):
        self.task_queue.append(task)