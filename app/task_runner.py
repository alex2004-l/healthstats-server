import os
import json
from queue import Queue, Empty
from threading import Thread, Event, Lock
from app.task import TaskInterface


class ThreadPool:
    ''' Custom threadpool implementation'''
    def __init__(self):
        self.num_threads = os.environ.get('TP_NUM_OF_THREADS', os.cpu_count())
        self.threads = [TaskRunner(self) for _ in range(self.num_threads)]

        # The running tasks are kept in a queue
        self.running_tasks = Queue()

        # All the tasks are kept in a dictionary
        self.total_tasks = {}
        self.dict_lock = Lock()

        # Event for signaling shutdown
        self.shutdown = Event()

    def start(self):
        '''Starts all threads from the threadpool'''
        for thread in self.threads:
            thread.start()

    def submit_task(self, task : TaskInterface):
        '''Adds a new task to the queue and adds an entry in the dictionary'''
        self.running_tasks.put(task)
        with self.dict_lock:
            self.total_tasks[task.id] = "running"

    def get_task(self) -> TaskInterface:
        '''Tries to get a task element from the queue'''
        # Waits 0.25s and raises and Empty error if no element is added
        return self.running_tasks.get(timeout=0.25)

    def complete_task(self, id_task : int):
        '''Updates inner counter of queue and dictionary entry for a task'''
        self.running_tasks.task_done()
        with self.dict_lock:
            self.total_tasks[id_task] = "done"

    def get_task_status(self, id_task : int) -> str:
        '''Returns the status of a task'''
        return self.total_tasks[id_task]

    def get_server_status(self) -> bool:
        '''Return false if the server is shutdown and true if it's up'''
        if self.shutdown.is_set():
            return False
        return True

    def get_tasks_status(self):
        '''Returns a formated list of all the tasks'''
        return [{f'job_id_{i}': self.total_tasks[i]} for i in range(1, len(self.total_tasks))]

    def count_pending_tasks(self):
        '''Returns the size of the inner queue'''
        return self.running_tasks.qsize()

    def graceful_shutdown(self):
        '''Shutdown function'''
        self.shutdown.set()

        # Joining all the threads
        for thread in self.threads:
            thread.join()


class TaskRunner(Thread):
    '''Custom thread implementation'''
    def __init__(self, threadpool : ThreadPool):
        super().__init__()
        self.threadpool = threadpool
        self.current_task = None

    def run(self):
        '''The loop executed by the threads in the pool'''
        while True:
            try:
                if not self.threadpool.get_server_status() and self.threadpool.count_pending_tasks() == 0:
                    break

                # Tries to get an element from the queue
                self.current_task = self.threadpool.get_task()

                # Solve and write result
                result = self.current_task.func()
                self.write_file(result)

                # Mark as complete
                self.threadpool.complete_task(self.current_task.id)
            except Empty:
                continue

    def write_file(self, result):
        '''Auxiliary method for writing a file'''
        file_path = os.path.join("results", f"job_id_{self.current_task.id}.json")
        with open(file_path, "w", encoding= 'UTF-8') as f:
            json.dump(result, f)
