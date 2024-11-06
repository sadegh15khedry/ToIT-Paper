import random
import gymnasium as gym 

def q_learning_algorithm(vehicles, edge_servers):
    actions = [0, 1] # 1 for offloading and 0 for local execution
    state = []
    

def manage_offloading(vehicles, edge_servers, algorithm):
    if algorithm == "greedy_local":
        print ("Greedy Local Offloading Algorithm")
    elif algorithm == "random":
        print ("Random")
    elif algorithm == "greedy_offloading":
        print ("Greedy Offloading Algorithm")
    elif algorithm == "Q-learning":
        print ("Q-Learning")
        q_learning_algorithm(vehicles, edge_servers)
        
    