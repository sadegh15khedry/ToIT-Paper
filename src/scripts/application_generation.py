from application import Application
from task import Task

def generate_aplplication_tasks(app, vehicle):
    tasks = []
    for i in range(0,6):
        task = Task(i, app.id, vehicle.id, 10, 10, False)
        task.print_task_info()
        tasks.append(task)
    app.unfinished_tasks = tasks
    app.edges

def generate_application_task_edges(app):
    edges = [
                [0, 1, 1, 0, 0, 0],
                [0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0]
            ]
    app.edges = edges

def generate_an_application (vehicle):
    app = Application(vehicle.get_new_app_id(), vehicle.id, 0, 1, None, None)
    generate_aplplication_tasks(app, vehicle)
    generate_application_task_edges(app)
    
    app.print_application_info()
    vehicle.unfinished_applications.append(app)
    
    

def vehicles_applicaton_generation(vehicles):
    for vehicle in vehicles:
        generate_an_application(vehicle)