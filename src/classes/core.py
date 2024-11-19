class Core:
    def __init__(self, id, frequency):
        self.id = id
        self.frequency = frequency
        self.task_queue = []
        self.runnig_task = None
    
        
    def add_task(self, task):
        self.task_queue.append(task)
        
    
    def run_new_task(self, time):
        if self.task_queue and self.running_task is None:
            task = self.task_queue.pop(0)
            task.start_time = time
            self.running_task = task

            
            
    def is_busy(self, time):
        task = self.running_task
        if task == None:
            return False
        
        is_finished = task.is_finished(time)
        if is_finished:
            self.finished_tasks.append(task)
            self.running_task = None
            task.device.handle_task_finish(task, time)
            return False
        return True        