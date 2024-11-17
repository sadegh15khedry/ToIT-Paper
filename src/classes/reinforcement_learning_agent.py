import random
import numpy as np

class ReinforcementLearningAgent():
    alpha = 0.1
    gamma = 0.9
    epsilon = 1.0
    epsilon_min = 0.01
    epsilon_decay = 0.995
    number_of_task_sizes = 3
    number_of_execution_cycles = 3
    max_queue_length = 3
    number_of_distance_ranges=3
    should_update_q_table = None
    actions = [0, 1] # 0 for local execution and  for offloading and 
    q_table = np.zeros((number_of_task_sizes, number_of_execution_cycles, max_queue_length,number_of_distance_ranges, len(actions)))
    def __init__(self, vehicle):
        # RL hyperparameters

        
        # self.updated_state_indices_list = []
        # self.not_updated_state_indices_list = []
        # self.state_indices_list = []
        # self.actions_list = []
        # self.tasks_list = []
        self.counter = 0
        self.history = []
        
        
        self.vehicle = vehicle

        
        
    def discretize_task_size(self, task_size):
        if 2000000 <= task_size and task_size <= 4000000:
            return 0
        elif  5000000 <= task_size and task_size <= 7000000:
            return 1
        elif  8000000 <= task_size and task_size <= 10000000:
            return 2
        else:
            raise ValueError(f"Invalid task size: {task_size}")
        
    def discretize_execution_cycles(self, cycle):
        if 2*(10**9) <= cycle and cycle <= 4*(10**9):
            return 0
        elif  5*(10**9) <= cycle and cycle <= 7*(10**9):
            return 1
        elif  8*(10**9) <= cycle and cycle <= 10*(10**9):
            return 2
        else:
            raise ValueError(f"Invalid execution time: {cycle}")

    def discretize_queue_length(self, queue_length):
        if 0 <= queue_length and  queue_length <= 5:
            return 0
        elif 5 < queue_length and queue_length<=20:
            return 1
        elif 20 < queue_length:
            return 2
        else:
            raise ValueError(f"Invalid queue length: {queue_length}")

    def discretize_distance(self, distance):
        if 0 <= distance and  distance <= 100:
            return 0
        elif 100 < distance and distance<=200:
            return 1
        elif 200 < distance:
            return 2
        else:
            raise ValueError(f"Invalid queue length: {distance}")

    
    def discretize_state(self, state_values):
        task_size_state = self.discretize_task_size(state_values['task_size'])
        execution_time_state = self.discretize_execution_time(state_values['execution_time'])
        queue_length_state = self.discretize_queue_length(state_values['queue_length'])
        distance_state=self.discretize_distance(state_values['distance'])
        return (task_size_state, execution_time_state, queue_length_state,distance_state)

    def store_previous_task(self, task):
        self.previous_task = task
        
    def choose_action(self, task, queue_length,distance):#state_indices
        
        self.counter += 1
        state_indices = (self.discretize_task_size(task.size),
                         self.discretize_execution_cycles(task.execution_cycles),
                         self.discretize_queue_length(queue_length),
                         self.discretize_distance(distance))
        
        
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
        if ReinforcementLearningAgent.should_update_q_table == True:
            history_row = { "id": self.counter,"task": task, "state_indices": state_indices, "action": action, "reward": None, "is_updated": False }
            self.history.append (history_row)
            self.check_if_need_to_update_q_table()
        return action
    
    def update_q_table(self, before_state_indices, before_task, before_action, after_state_indices):
        print("To calculate reward----> Vehicle->",before_task.vehicle.id,"  Task:",before_task.id, "Response time:",before_task.response_time, "   Energy:",before_task.energy, " , Before state indices:",before_state_indices)
        reward = -0.5*(before_task.response_time)- 0.5 * before_task.energy  # negative reward for execution time
        current_q = self.q_table[before_state_indices][before_action]
        max_future_q = np.max(self.q_table[after_state_indices])
        new_q = current_q + self.alpha * (reward + self.gamma * max_future_q - current_q)
        self.q_table[before_state_indices][before_action] = new_q
        #self.updated_state_indices_list.append(before_state_indices)
        print("Q-table updated!!!!!!!!")
        print(self.q_table)

        
    
    def check_if_need_to_update_q_table(self):
        # print(self.history)
        if len(self.history) < 2:
            return
        size = len(self.history)
        for index, row in  enumerate(self.history):
            if row["is_updated"] == False and row["task"].end_time != None and index+1 != size:
                before_state_indices = row["state_indices"]
                after_state_indices = self.history[index+1]["state_indices"]
                self.update_q_table(before_state_indices, row["task"], row["action"], after_state_indices)
                row["is_updated"] = True