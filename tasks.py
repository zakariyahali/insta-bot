import threading
import time
import requests

def schedule_posting():
    while True:
        response = requests.post("http://localhost:8000/generate-and-post")
        print(response.json())
        time.sleep(20 * 60)  # Sleep for 20 minutes

def start_scheduler():
    thread = threading.Thread(target=schedule_posting)
    thread.start()
