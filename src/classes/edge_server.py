class EdgeServer:
    def __init__(self, id, x, y, frequency, bandwidth):
        self.id = id
        self.runnig_task = None
        self.x = x
        self.y = y
        self.frequency = frequency
        self.task_queue = []
        self.channel = []
        self.finished_tasks = []
        self.bandwidth = bandwidth 
        
    # def print_edge_server_info(self):
    #     print(f"Edge server Id: {self.id}, x:{self.x}, y:{self.y}")


    def check_channel(self, time):
        for task in self.channel:
            if time == task.release_time + int(task.size/self.bandwidth):
                self.channel.remove(task)
                self.task_queue.append(task)
                # print (f"task:{task.id} has been reached edge_server:{self.id}")
    
                
    def run_new_task(self, time):
        if self.task_queue and self.runnig_task is None:
            task = self.task_queue.pop(0)
            task.start_time = time
            self.runnig_task = task
            # print (f"task:{task.id} is now runnig on edge_server:{self.id}")
            
            
    def is_busy(self, time):
        task = self.runnig_task
        if task == None:
            return False
        
        is_finished = task.is_finished(time)
        if is_finished:
            self.finished_tasks.append(task)
            self.runnig_task = None
            task.vehicle.handle_task_finish(task, time)
            # print(f"task:{task.id} is finished processing on edge_server:{self.id}")
            return False
        return True


        
