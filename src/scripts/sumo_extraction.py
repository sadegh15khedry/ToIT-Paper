import xml.etree.ElementTree as ET
import pandas as pd

def extract_location_direction_speed(xml_file_path, save_path):
    # Load the FCD output file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Extract location (x, y), speed, and angle (direction) for each vehicle at each timestep
    data = []
    
    for timestep in root.findall('timestep'):
        # Convert time to int and adjust to start from 0
        time = int(float(timestep.get('time')) - 1)  # Subtract 1 to start from 0
        for vehicle in timestep.findall('vehicle'):
            vehicle_id = vehicle.get('id')
            
            # Remove 'veh' prefix, convert vehicle_id to int, and add 1 to start from 1
            if vehicle_id.startswith('veh'):
                vehicle_id = int(vehicle_id.replace('veh', '')) + 1
            
            speed = float(vehicle.get('speed'))
            angle = float(vehicle.get('angle'))  # Angle represents the direction in degrees
            x = float(vehicle.get('x'))  # x coordinate
            y = float(vehicle.get('y'))  # y coordinate
            
            data.append({
                'time': time,  # Now time starts from 0
                'vehicle_id': vehicle_id,  # Now it's an integer starting from 1
                'speed': speed,
                'angle': angle,
                'x': x,
                'y': y
            })

    # Convert to a DataFrame for analysis
    df = pd.DataFrame(data)
    
    # Save the DataFrame to a CSV file
    df.to_csv(save_path, index=False)
    
    # Display or analyze the DataFrame
    print(df.head())  # View the first few rows

    # Example: Analyze average speed and direction
    avg_speed = df['speed'].mean()
    print(f'Average Speed: {avg_speed:.2f} m/s')

    # Example: Group by vehicle and calculate the average direction
    avg_direction_by_vehicle = df.groupby('vehicle_id')['angle'].mean()
    print(avg_direction_by_vehicle)

