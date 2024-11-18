import random

def generate_tasks(devices, time):
    for device in devices:
        device.generate_task(time)
 
def get_action(device, task, distance, algorithm):
    action = None
    if(algorithm == 'proposed'):
        action = device.agent.choose_action(task, len(device.local_execution_queue),distance)
    elif (algorithm == 'local_only'):
        action = 0
    elif (algorithm == 'offload_only'):
        action = 1
    elif (algorithm == 'random'):
        action = random.randrange(0, 2)
    # print(action)
    return action

        
def handle_undecided_tasks(device, edge_servers, algorithm):
    for task in device.undecided_tasks:
        closest_edge_server, distance = device.find_closest_edge_server(edge_servers)
        action = get_action(device, task, distance, algorithm)
        
        device.undecided_tasks.remove(task)
        if(action == 0):
            task.execution_location = 0
            task.set_execution_time(device.frequency)
            task.add_execution_energy(device.frequency)
            task.distance = distance   
            device.local_execution_queue.append(task)
        elif(action == 1):

            device.unfinished_offload_tasks.append(task)

            task.execution_location = 1
            task.set_execution_time(closest_edge_server.frequency)
            task.add_transmission_energy(device.transmission_power, closest_edge_server.bandwidth, distance)
            task.set_transmission_time(closest_edge_server.bandwidth, distance,device.transmission_power)
            task.distance = distance
            closest_edge_server.channel.append(task)
            

            
            



def manage_tasks(devices, edge_servers, time, algorithm):

    for device in devices:
        handle_undecided_tasks(device, edge_servers, algorithm)
        is_busy = device.is_busy(time)
        if is_busy == False:
            device.run_new_task(time)
    
    for edge_server in edge_servers:
        edge_server.check_channel(time)
        is_busy = edge_server.is_busy(time)
        if is_busy == False:
            edge_server.run_new_task(time)
        