class EdgeServer:
    def __init__(self, id, cores, x, y, bandwidth):
        self.id = id
        self.running_task = None
        self.x = x
        self.y = y
        self.cores = cores
        self.task_queue = []
        self.channel = []
        self.finished_tasks = []
        self.bandwidth = bandwidth
        


    def check_channel(self, time):
        for task in self.channel:
            if time == task.release_time + task.transmission_time:
                # print(f"++++++++++ reached  ++++++++++++++++++++++++time: {time}, release time: {task.release_time}, transmission_time:{task.transmission_time}")
                self.channel.remove(task)
                self.task_queue.append(task)
                # print (f"task:{task.id} has been reached edge_server:{self.id}")
    
                



        
