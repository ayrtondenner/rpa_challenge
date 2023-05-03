from datetime import datetime

def print_debug_log(message):
    print(f"{str(datetime.now())} - {message}")