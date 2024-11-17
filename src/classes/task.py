import math
class Task:
    v1=10**-3
    v2=4
    noise= 1.6*(10**-11)
    def __init__(self, id, vehicle, release_time, execution_cycles, size):
        self.id = id
        self.vehicle = vehicle
        self.release_time = release_time
        self.response_time = None
        self.transmission_time = 0
        self.size = size  # in MBs
        self.execution_time = None
        self.execution_cycles = execution_cycles
        self.start_time = None
        self.end_time = None
        self.energy = 0
        self.execution_energy=0
        self.transfer_energy=0
        self.execution_location = None
        self.transfer_rate=0

    def is_finished(self, time):
        if self.start_time + self.execution_time == time:
            self.end_time = time
            self.response_time = self.end_time - self.release_time
            return True
        return False
            
    # def print_task_info(self):
        # print(f"Task ID: {self.id}, Execution Time: {self.execution_time} seconds")

    def set_execution_time(self, frequency):
        self.execution_time = (self.execution_cycles  / frequency) * 1000
        self.execution_time = math.ceil(self.execution_time)# in milicseconds
        # print(f"Execution Time: {self.execution_time} miliseconds")
        
    def add_execution_energy(self, frequency):
        execution_energy= (10**-28)*(frequency ** 2)*(self.execution_cycles)
        self.execution_energy=execution_energy
        # print(f"id:{self.id} E_ex:{execution_energy}")
        self.energy += execution_energy # in Joules    
    
    
    def add_transmission_energy(self, trasmission_power, bandwidth, distance):
        transmission_energy= (trasmission_power * self.size) / self.calc_transfer_rate(bandwidth,distance,trasmission_power)
        self.transfer_energy=transmission_energy
        # print(f"id:{self.id} E_tr:{transmission_energy}")
        self.energy += transmission_energy  # in Joules
        
    
    def set_transmission_time(self, bandwidth, distance,trasmission_power):
        transmission_time=self.size / self.calc_transfer_rate(bandwidth, distance,trasmission_power)
        transmission_time *= 1000
        transmission_time =  round(transmission_time)
        # print(f"id:{self.id} T_tr:{transmission_time}")
        self.transmission_time = transmission_time 

    def calc_transfer_rate(self,bandwidth, distance,trasmission_power):
        # print("/\/\/\/\/\/\/\/\/\/calculate RATE")
        # print(f"distance:{distance}, v1:{Task.v1}, v2:{Task.v2}, power{trasmission_power}, Noise{Task.noise}, bandwidth{bandwidth}")
        
        rate=bandwidth* math.log2(1+(Task.v1*(distance**(-Task.v2))*trasmission_power)/Task.noise)
        self.transfer_rate=rate
        # print(f"id:{self.id} Transfer rate:{rate}")
        return rate 