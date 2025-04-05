from queue import Queue
from threading import Thread, Event
from app.task import TaskInterface
import time
import os
import json

class ThreadPool:
    def __init__(self):
        self.num_threads = os.environ.get('TP_NUM_OF_THREADS', os.cpu_count())
        self.threads = [TaskRunner(self) for _ in range(self.num_threads)]

        self.running_tasks = Queue()
        self.total_tasks = {}

        # TODO : add an event for graceful shutdown
        self.shutdown = Event()
    
    def start(self):
        for thread in self.threads:
            thread.start()
        
    def submit_task(self, task : TaskInterface):
        self.running_tasks.put(task)
        self.total_tasks[task.id] = "running"

    def get_task(self) -> TaskInterface:
        self.running_tasks.get()
    
    def complete_task(self, id : int):
        self.total_tasks[id] = "done"
        self.running_tasks.task_done()


class TaskRunner(Thread):
    def __init__(self, threadpool : ThreadPool):
        super().__init__()
        self.threadpool = threadpool
        self.current_task = None

    def run(self):
        while True:
            self.current_task = self.threadpool.running_tasks.get_task()
            # Execute the job and save the result to disk
            result = self.current_task.run()
            self.write_file(result)
            self.threadpool.complete_task(self.current_task.id)
    
    def write_file(self, result):
        file_path = os.path.join("results", f"job_id_{self.current_task.id}.json")

        with open(file_path, "w") as f:
            json.dump(result, f)


