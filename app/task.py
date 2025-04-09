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
        return self.data_ingestor.get_mean_values_for_all_states(self.question)

class TaskStateMean(TaskInterface):
    def func(self):
        return self.data_ingestor.get_mean_value_for_state(self.question, self.state)

class TaskBest5(TaskInterface):
    def func(self):
        all_states = self.data_ingestor.get_mean_values_for_all_states(self.question)
        is_min = self.data_ingestor.check_question_best_is_min(self.question)
        return dict(sorted(all_states.items(), key=lambda item: item[1], reverse=not is_min)[:5])

class TaskWorst5(TaskInterface):
    def func(self):
        mean_all_states = self.data_ingestor.get_mean_values_for_all_states(self.question)
        is_min = self.data_ingestor.check_question_worst_is_min(self.question)
        return dict(sorted(mean_all_states.items(), key=lambda item: item[1], reverse=not is_min)[:5])

class TaskGlobalMean(TaskInterface):
    def func(self):
        return {"global_mean" : self.data_ingestor.get_global_mean(self.question)}

class TaskDiffFromMean(TaskInterface):
    def func(self):
        mean_all_states = self.data_ingestor.get_mean_values_for_all_states(self.question)
        global_mean = self.data_ingestor.get_global_mean(self.question)
        return {state: global_mean - value for state, value in mean_all_states.items()}

class TaskStateDiffFromMean(TaskInterface):
    def func(self):
        mean_state = self.data_ingestor.get_mean_value_for_state(self.question, self.state)
        global_mean = self.data_ingestor.get_global_mean(self.question)
        return {self.state : global_mean - mean_state}

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
        "diff_from_mean": TaskDiffFromMean,
        "state_diff_from_mean": TaskStateDiffFromMean,
        "mean_by_category": TaskMeanByCategory,
        "state_mean_by_category": TaskStateMeanByCategory
    }

    @staticmethod
    def create_task(task_type : str ,id : int, question : str, data_ingestor, state : str = None) -> TaskInterface:
        if task_type in TaskFactory._task_types:
            return TaskFactory._task_types[task_type](id, question, data_ingestor, state)
        else:
            raise Exception("Unknown task")