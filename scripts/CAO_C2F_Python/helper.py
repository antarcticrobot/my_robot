from datetime import datetime

def get_time():
    now = datetime.now()
    now = now.strftime("%y_%m_%d_%H_%M_%S%f")
    return now