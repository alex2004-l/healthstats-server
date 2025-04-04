from queue import Queue
from threading import Thread, Event
import time
import os

class ThreadPool:
    def __init__(self):
        self.num_threads = os.environ.get('TP_NUM_OF_THREADS', os.cpu_count())
        self.threads = [TaskRunner(self) for _ in range(self.num_threads)]

        self.running_tasks = Queue()
        self.total_tasks = {}

        # TODO : add an event for graceful shutdown
    
    def start(self):
        for thread in self.threads:
            thread.start()
        
    def submit(self):
        pass


class TaskRunner(Thread):
    def __init__(self, threadpool : ThreadPool):
        # TODO: init necessary data structures
        super().__init__()
        self.threadpool = threadpool

    def run(self):
        while True:
            # TODO
            # Get pending job
            # Execute the job and save the result to disk
            # Repeat until graceful_shutdown
            pass
