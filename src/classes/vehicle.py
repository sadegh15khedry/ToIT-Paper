class Vehicle:
    def __init__(self, id, x, y, speed, direction, cores, memory, bandwidth):
        self.id = id
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.unfinished_applications = []
        self.finished_applications = []
        self.cores = cores
        self.memory = memory
        self.bandwidth = bandwidth
        self.new_app_id = 0
        
    def add_task(self, application):
        self.unfinished_applications.append(application)
        
    def remove_task(self, application):
        if application in self.unfinished_applications:
            self.unfinished_applications.remove(application)
            
    def add_finished_task(self, application):
        self.finished_applications.append(application)
        
        
    def get_new_app_id(self):
        self.new_app_id += 1
        return self.new_app_id
         
    def print_vehicle_info(self):
        print(f"id: {self.id}, x: {self.x}, y: {self.y}, speed: {self.speed}, direction: {self.direction}, speed: {self.speed}")
    