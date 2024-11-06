
def check_core_for_finished_task(core, time):
    task = core.runnig_task
    if task is None:
        return False
    if task.is_finished():
        core.running_task = None
        print(f" Core {core.id} has finished a task")

def assign_new_task_to_core(core, time):
    core.running_task = core.task_queue.pop(0)
    core.running_task.start_time = time
    print(f"Core {core.id} has assigned a new task")        

# def manage_vehicle_tasks(vehicle, edge_servers):
#     print ("Managing vehicle tasks")

# def add_to_vehicles_finished_tasks(edge_server, task):

def check_for_finished_edge_server_tasks(edge_server, vehicles, time):
    for core in edge_server.cores:
        if check_core_for_finished_task(core, time):
            print("finished task")
            # add_to_vehicles_finished_tasks()
            # schedule_next_edge_server_task(edge_server, core)

def assign_new_task_to__edge_server(edge_server, time):
    # temporary assiging the first task
    for core in edge_server.cores:
        if core.running_task is None and core.task_queue:
            assign_new_task_to_core(core, time)
        
            


def check_for_finished_vehicle_tasks(vehicle, time):
    for core in vehicle.cores:
         if check_core_for_finished_task(core, time):
            print("finished task")
            
            
def assign_new_task_in_vehicle(vehicle, time):
    for core in vehicle.cores:
        if core.running_task is None and core.task_queue:
            assign_new_task_to_core(core, time)

def manage_tasks(vehicles, edge_servers, time):
    for vehicle in vehicles:
        check_for_finished_vehicle_tasks(vehicle, time)
        assign_new_task_in_vehicle(vehicle, time)
        
    for edge_server in edge_servers:
        check_for_finished_edge_server_tasks(edge_server, vehicles, time)
        assign_new_task_to__edge_server(edge_server, time)
        