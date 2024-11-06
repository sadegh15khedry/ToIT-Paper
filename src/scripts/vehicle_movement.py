
import pandas as pd

def move_vehicle(vehicle, time_step_movements): 
    vehicle_movement_info = time_step_movements[time_step_movements['vehicle_id'] == vehicle.id]
    if not vehicle_movement_info.empty:
        vehicle_movement_info = time_step_movements[time_step_movements['vehicle_id'] == vehicle.id].iloc[0]
    vehicle.x = vehicle_movement_info.x
    vehicle.y = vehicle_movement_info.y
    vehicle.direction = vehicle_movement_info.angle
    vehicle.speed = vehicle_movement_info.speed
    if(vehicle.id == 1):
        vehicle.print_vehicle_info()
    
def get_time_step_movements(time_step, mobility_file_path):
    time_step_csv = mobility_file_path[mobility_file_path['time'] == time_step]
    return time_step_csv
    
def vehicle_movement_funciton(vehicles, time_step, mobility_file):
    time_step_movements = get_time_step_movements(time_step, mobility_file)
    for vehicle in vehicles:
        move_vehicle(vehicle, time_step_movements)
        
def load_mobility_csv(path):
    file = pd.read_csv(path)
    return file
