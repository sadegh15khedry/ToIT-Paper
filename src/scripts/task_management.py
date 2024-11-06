 
def generate_tasks(vehicles, time):
    for vehicle in vehicles:
        vehicle.generate_task(time)
 

    
def vehicles_task_generation(vehicles, time):
    
    for vehicle in vehicles:
        vehicle.generate_task(time)
        
def handle_undecided_tasks(vehicle, edge_servers):
    for task in vehicle.undecided_tasks:
        action = vehicle.agent.choose_action(task, len(vehicle.local_execution_queue))
        vehicle.undecided_tasks.remove(task)
        if(action == 0):
            task.execution_location = 0
            task.set_execution_time(vehicle.frequency)
            task.add_execution_energy(vehicle.frequency)
            vehicle.local_execution_queue.append(task)
            print(f"task: {task.id} locaction: local at {vehicle.id}, energy:{task.energy}, execution_time:{task.execution_time}")
        elif(action == 1):
            # print(f"task energy {task.energy} ")
            vehicle.unfinished_offload_tasks.append(task)
            closest_edge_server = vehicle.find_closest_edge_server(edge_servers)
            task.execution_location = 1
            task.set_execution_time(closest_edge_server.frequency)
            task.add_transmission_energy(vehicle.transmission_power, closest_edge_server.bandwidth)
            # task.add_execution_energy(closest_edge_server.frequency)
            closest_edge_server.channel.append(task)
            print(f"task: {task.id} locaction: edge_server {closest_edge_server.id}, energy:{task.energy}, execution_time:{task.execution_time}")
            



def manage_tasks(vehicles, edge_servers, time):

    for vehicle in vehicles:
        handle_undecided_tasks(vehicle, edge_servers)
        is_busy = vehicle.is_busy(time)
        if is_busy == False:
            vehicle.run_new_task(time)
    
    for edge_server in edge_servers:
        edge_server.check_channel(time)
        is_busy = edge_server.is_busy(time)
        if is_busy == False:
            edge_server.run_new_task(time)
        