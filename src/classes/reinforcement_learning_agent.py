import random
import numpy as np

class ReinforcementLearnigAgent():
    
    def __init__(self, vehicle):
        # RL hyperparameters
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        
        # self.updated_state_indices_list = []
        # self.not_updated_state_indices_list = []
        # self.state_indices_list = []
        # self.actions_list = []
        # self.tasks_list = []
        self.counter = 0
        self.history = []
        
        self.nember_of_task_sizes = 3
        self.number_of_execution_cycles = 3
        self.max_queue_length = 10
        self.vehicle = vehicle

        self.actions = [0, 1] # 0 for local execution and  for offloading and 
        self.q_table = np.zeros((self.nember_of_task_sizes, self.number_of_execution_cycles, self.max_queue_length, len(self.actions)))
        
        
    def discretize_task_size(self, task_size):
        if task_size == 2000000:
            return 0
        elif task_size == 5000000:
            return 1
        elif task_size == 7000000:
            return 2
        else:
            raise ValueError(f"Invalid task size: {task_size}")
        
    def discretize_execution_cycles(self, execution_time):
        if execution_time == 2000000:
            return 0
        elif execution_time == 5000000:
            return 1
        elif execution_time == 7000000:
            return 2
        else:
            raise ValueError(f"Invalid execution time: {execution_time}")

    def discretize_queue_length(self, queue_length):
        if 0 <= queue_length and  queue_length <= self.max_queue_length:
            return int(queue_length)
        else:
            raise ValueError(f"Invalid queue length: {queue_length}")

    def discretize_state(self, state_values):
        task_size_state = self.discretize_task_size(state_values['task_size'])
        execution_time_state = self.discretize_execution_time(state_values['execution_time'])
        queue_length_state = self.discretize_queue_length(state_values['queue_length'])
        return (task_size_state, execution_time_state, queue_length_state)

    def store_previous_task(self, task):
        self.previous_task = task
        
    def choose_action(self, task, queue_length):#state_indices
        
        self.counter += 1
        state_indices = (self.discretize_task_size(task.size),
                         self.discretize_execution_cycles(task.execution_cycles),
                         self.discretize_queue_length(queue_length))
        
        
        # check_if_need_to_update_q_table()
        # if len(self.state_indices_list) > 1:
        #     self.update_q_tabel()
        # self.prvious_state_indices = state_indices
            
        if np.random.rand() < self.epsilon:
            action = np.random.choice(self.actions)
        else:
            action = np.argmax(self.q_table[state_indices])
        
        # self.actions_list.append(action) #for update_q_table later
        # self.state_indices_list.append(state_indices)
        # self.not_update_q_table_tasks_list.append(task)
        history_row = { "id": self.counter,"task": task, "state_indices": state_indices, "action": action, "reward": None, "is_updated": False }
        self.history.append (history_row)
        self.check_if_need_to_update_q_table()
        return action
    
    def update_q_tabel(self, before_state_indices, before_task, before_action, after_state_indices):
        reward = -0.5*(before_task.end_time- before_task.start_time)- 0.5 * before_task.energy  # negative reward for execution time
        current_q = self.q_table[before_state_indices][before_action]
        max_future_q = np.max(self.q_table[after_state_indices])
        new_q = current_q + self.alpha * (reward + self.gamma * max_future_q - current_q)
        self.q_table[before_state_indices][before_action] = new_q
        #self.updated_state_indices_list.append(before_state_indices)
        print("Q-table updated!!!!!!!!")
        
    
    def check_if_need_to_update_q_table(self):
        # print(self.history)
        if len(self.history) < 2:
            return
        size = len(self.history)
        for index, row in  enumerate(self.history):
            if row["is_updated"] == False and row["task"].end_time != None and index+1 != size:
                before_state_indices = row["state_indices"]
                after_state_indices = self.history[index+1]["state_indices"]
                self.update_q_tabel(before_state_indices, row["task"], row["action"], after_state_indices)
                row["is_updated"] = True