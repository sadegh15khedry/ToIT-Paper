import pandas as pd

def save_report(devices, report_path):
    header=["device_id","task_id","execution_location","size", "distance", "transfer_rate", "execution_cycles","start_time","end_time","release_time"
            ,"response_time","transmission_time","execution_time","execution_energy","transfer_energy","total_energy"]
    file_list = [header]
    save_list_to_csv(header,report_path)
    for device in devices:
        for task in device.finished_tasks:
            row = []
            row=[device.id, task.id, task.execution_location, task.size, task.distance, task.transfer_rate, task.execution_cycles, task.start_time, task.end_time, task.release_time, task.response_time, task.transmission_time, task.execution_time, task.execution_energy, task.transfer_energy, task.energy]
            file_list.append(row)
    
    save_list_to_csv(file_list,report_path)


def save_list_to_csv(list_data, file_path):
    df = pd.DataFrame(list_data)
    df.to_csv(file_path, index=False, header=False)