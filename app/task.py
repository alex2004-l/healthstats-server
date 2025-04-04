from __future__ import annotations
from abc import ABC, abstractmethod

class TaskInterface(ABC):
    def __init__(self, id : int, question: str, state: str = None):
        self.id = id
        self.result = None
        self.question = question
        self.state = state

    @abstractmethod
    def func(self):
        pass


class TaskStatesMean(TaskInterface):
    def __init__(self, id, question, state = None):
        super().__init__(id, question, state)

    def func(self):
        pass


class TaskStateMean(TaskInterface):
    def __init__(self, id, question, state = None):
        super().__init__(id, question, state)

    def func(self):
        pass


class TaskBest5(TaskInterface):
    def __init__(self, id, question, state = None):
        super().__init__(id, question, state)

    def func(self):
        pass


class TaskWorst5(TaskInterface):
    def __init__(self, id, question, state = None):
        super().__init__(id, question, state)

    def func(self):
        pass


class TaskGlobalMean(TaskInterface):
    def __init__(self, id, question, state = None):
        super().__init__(id, question, state)

    def func(self):
        pass


class TaskStatesDiffFromMean(TaskInterface):
    def __init__(self, id, question, state = None):
        super().__init__(id, question, state)

    def func(self):
        pass


class TaskMeanByCategory(TaskInterface):
    def __init__(self, id, question, state = None):
        super().__init__(id, question, state)

    def func(self):
        pass


class TaskStateMeanByCategory(TaskInterface):
    def __init__(self, id, question, state = None):
        super().__init__(id, question, state)

    def func(self):
        pass


class TaskFactory:
    _task_types = {
        "states_mean": TaskStatesMean,
        "state_mean": TaskStateMean,
        "best5": TaskBest5,
        "worst5": TaskWorst5,
        "global_mean": TaskGlobalMean,
        "states_diff_from_mean": TaskStatesDiffFromMean,
        "mean_by_category": TaskMeanByCategory,
        "state_mean_by_category": TaskStateMeanByCategory
    }

    @staticmethod
    def create_task(task_type : str ,id : int, question : str, state : str = None) -> TaskInterface:
        if task_type in TaskFactory._task_types:
            return TaskFactory._task_type[type](id, question, state)
        else:
            raise Exception("Unknown task")