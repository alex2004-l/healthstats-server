from __future__ import annotations
from abc import ABC, abstractmethod
from app.data_ingestor import DataIngestor

class TaskInterface(ABC):
    def __init__(self, id : int, question: str, data_ingestor : DataIngestor, state: str = None):
        self.id = id
        self.result = None
        self.question = question
        self.state = state
        self.data_ingestor = data_ingestor

    @abstractmethod
    def func(self):
        pass


class TaskStatesMean(TaskInterface):
    def func(self):
        df = self.data_ingestor.get_df_by_question(self.question)
        result = df.groupby("LocationDesc")["Data_Value"].mean().sort_index().to_dict()
        return result


class TaskStateMean(TaskInterface):
    def func(self):
        pass


class TaskBest5(TaskInterface):
    def func(self):
        pass


class TaskWorst5(TaskInterface):
    def func(self):
        pass


class TaskGlobalMean(TaskInterface):
    def func(self):
        pass


class TaskStatesDiffFromMean(TaskInterface):
    def func(self):
        pass


class TaskMeanByCategory(TaskInterface):
    def func(self):
        pass


class TaskStateMeanByCategory(TaskInterface):
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
            return TaskFactory._task_types[type](id, question, state)
        else:
            raise Exception("Unknown task")