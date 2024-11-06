import math
class Task:
    def __init__(self, id, vehicle, relese_time, execution_cycles, size):
        self.id = id
        self.vehicle = vehicle
        self.release_time = relese_time
        self.size = size  # in MBs
        self.execution_time = None
        self.execution_cycles = execution_cycles
        self.start_time = None
        self.end_time = None
        self.energy = 0
        self.execution_location = None

    def is_finished(self, time):
        if self.start_time + self.execution_time == time:
            self.end_time = time
            return True
        return False
            
    # def print_task_info(self):
        # print(f"Task ID: {self.id}, Execution Time: {self.execution_time} seconds")

    def set_execution_time(self, frequency):
        self.execution_time = (self.execution_cycles  / frequency) * 1000
        self.execution_time = math.ceil(self.execution_time)# in milicseconds
        # print(f"Execution Time: {self.execution_time} miliseconds")
        
    def add_transmission_energy(self, trasmission_power, bandwidth):
        self.energy += (trasmission_power * self.size) / bandwidth  # in Joules
        
    def add_execution_energy(self, frequency):
        self.energy += (10**-28)*(frequency ** 2)*(self.execution_cycles) # in Joules