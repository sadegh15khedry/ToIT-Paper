import json

def increment_iteration_number(config_data, old_iteration_number):
    new_iteration_number = old_iteration_number + 1
    
    # Save the updated iteration number back to the JSON file
    config_data['simulation_number'] = new_iteration_number
    with open('../config.json', 'w') as f:
        json.dump(config_data, f)

def get_simulation_number():
# Open the JSON file
    with open('../config.json', 'r') as f:
        # Load the JSON data into a Python dictionary
        config_data = json.load(f)
        iteration_number = config_data['simulation_number']
        # Increment the iteration number
        increment_iteration_number(config_data, iteration_number)
            
        # Return the updated iteration number
        return iteration_number
        