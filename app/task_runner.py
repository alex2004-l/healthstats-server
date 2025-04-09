import os
import json
import traceback
from queue import Queue, Empty
from threading import Thread, Event, Lock
from app.task import TaskInterface


class ThreadPool:
    def __init__(self):
        self.num_threads = os.environ.get('TP_NUM_OF_THREADS', os.cpu_count())
        self.threads = [TaskRunner(self, i) for i in range(self.num_threads)]

        self.running_tasks = Queue()
        self.total_tasks = {}
        self.dict_lock = Lock()

        self.shutdown = Event()

    def start(self):
        for thread in self.threads:
            thread.start()

    def submit_task(self, task : TaskInterface):
        self.running_tasks.put(task)
        with self.dict_lock:
            self.total_tasks[task.id] = "running"

    def get_task(self) -> TaskInterface:
        return self.running_tasks.get(timeout=0.25)

    def complete_task(self, id_task : int):
        self.running_tasks.task_done()
        with self.dict_lock:
            self.total_tasks[id_task] = "done"

    def get_task_status(self, id_task : int) -> str:
        return self.total_tasks[id_task]
    
    def get_server_status(self) -> bool:
        if self.shutdown.is_set():
            return False
        return True
    
    def get_tasks_status(self):
        return [{f'job_id_{i}': self.total_tasks[i]} for i in range(1, len(self.total_tasks))]
    
    def count_pending_tasks(self):
        return self.running_tasks.qsize()
    
    def graceful_shutdown(self):
        self.shutdown.set()

        for thread in self.threads:
            thread.join()


class TaskRunner(Thread):
    def __init__(self, threadpool : ThreadPool, thread_id):
        super().__init__()
        self.id = thread_id
        self.threadpool = threadpool
        self.current_task = None

    def run(self):
        while True:
            try:
                if not self.threadpool.get_server_status() and self.threadpool.count_pending_tasks() == 0:
                    break
                self.current_task = self.threadpool.get_task()
                result = self.current_task.func()
                self.write_file(result)
                self.threadpool.complete_task(self.current_task.id)
            except Empty:
                continue

    def write_file(self, result):
        file_path = os.path.join("results", f"job_id_{self.current_task.id}.json")
        with open(file_path, "w", encoding= 'UTF-8') as f:
            json.dump(result, f)
