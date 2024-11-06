class Task:
    def __init__(self, id, app_id, vehicle_id, execution_time, size, is_last_dag_task=False):
        self.id = id
        self.app_id = app_id
        vehicle_id = vehicle_id
        self.size = size  # in MBs
        self.execution_time = execution_time
        self.start_time = None
        self.end_time = None
        self.is_last_dag_task = is_last_dag_task

    def is_finished(self, time):
        if self.start_time + self.execution_time == time:
            self.end_time = time
            return True
        return False
            
    def print_task_info(self):
        print(f"Task ID: {self.id}, DAG ID: {self.app_id}, Execution Time: {self.execution_time} seconds, Is Last DAG Task: {self.is_last_dag_task}")

