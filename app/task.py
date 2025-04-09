from __future__ import annotations
from abc import ABC, abstractmethod
from app.data_ingestor import DataIngestor

class TaskInterface(ABC):
    '''Interface for tasks objects'''
    def __init__(self, id_task : int, question: str, data_ingestor : DataIngestor, state: str = None):
        self.id = id_task
        self.result = None
        self.question = question
        self.state = state
        self.data_ingestor = data_ingestor

    @abstractmethod
    def func(self):
        '''Specialized function for each child class that solves the task'''
        pass

class TaskStatesMean(TaskInterface):
    '''Task class that solves the states_mean query'''
    def func(self):
        return self.data_ingestor.get_mean_values_for_all_states(self.question)

class TaskStateMean(TaskInterface):
    '''Task class that solves the state_mean query'''
    def func(self):
        return self.data_ingestor.get_mean_value_for_state(self.question, self.state)

class TaskBest5(TaskInterface):
    '''Task class that solves the best_5 query'''
    def func(self):
        all_states = self.data_ingestor.get_mean_values_for_all_states(self.question)
        is_min = self.data_ingestor.check_question_best_is_min(self.question)
        return dict(sorted(all_states.items(), key=lambda item: item[1], reverse=not is_min)[:5])

class TaskWorst5(TaskInterface):
    '''Task class that solves the worst_5 query'''
    def func(self):
        mean_all_states = self.data_ingestor.get_mean_values_for_all_states(self.question)
        is_min = self.data_ingestor.check_question_worst_is_min(self.question)
        return dict(sorted(mean_all_states.items(), key=lambda item: item[1], reverse=not is_min)[:5])

class TaskGlobalMean(TaskInterface):
    '''Task class that solves the global_mean query'''
    def func(self):
        return {"global_mean" : self.data_ingestor.get_global_mean(self.question)}

class TaskDiffFromMean(TaskInterface):
    '''Task class that solves the diff_from_mean query'''
    def func(self):
        mean_all_states = self.data_ingestor.get_mean_values_for_all_states(self.question)
        global_mean = self.data_ingestor.get_global_mean(self.question)
        return {state: global_mean - value for state, value in mean_all_states.items()}

class TaskStateDiffFromMean(TaskInterface):
    '''Task class that solves the state_diff_from_mean query'''
    def func(self):
        mean_state = self.data_ingestor.get_mean_value_for_state(self.question, self.state)
        global_mean = self.data_ingestor.get_global_mean(self.question)
        return {state: global_mean - value for state, value in mean_state.items()}

class TaskMeanByCategory(TaskInterface):
    '''Task class that solves the mean_by_category query'''
    def func(self):
        mean_category_all_states = self.data_ingestor.get_mean_stratification(self.question)
        return {str(t) : value for t, value in mean_category_all_states.items()}

class TaskStateMeanByCategory(TaskInterface):
    '''Task class that solves the state_mean_by_category query'''
    def func(self):
        mean_cat_state = self.data_ingestor.get_mean_stratification_state(self.question, self.state)
        return {state : {str(t) : value for t, value in attr.items()} for state, attr in mean_cat_state.items()}

class TaskFactory:
    '''Factory pattern for generating tasks'''
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
    def create_task(task_type : str ,id_task : int, question : str, data_ingestor, state : str = None) -> TaskInterface:
        '''Creates and returns a new object that implements TaskInterface
        or raises an error if the type is unknown'''
        if task_type in TaskFactory._task_types:
            return TaskFactory._task_types[task_type](id_task, question, data_ingestor, state)
        raise Exception("Unknown task")
