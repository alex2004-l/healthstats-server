import unittest
from app.data_ingestor import DataIngestor
import app.task as task

PATH = "./unittests/dummy_data.csv"
QUESTION_DUPLICATE_STATES = 'Percent of adults aged 18 years and older who have obesity'
QUESTION_UNIQUE_STATES = 'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week'


class TestWebserver(unittest.TestCase):
    def setUp(self):
        self.data_ingestor = DataIngestor(PATH)
    
    def __assert_dicts_with_tolerance(self, actual, expected, tolerance = 0.00001):
        self.assertEqual(set(actual), set(expected))
        for key in expected:
            self.assertAlmostEqual(actual[key], expected[key], delta=tolerance)

    def test_best5_min_is_best(self):
        actual = task.TaskBest5(0, QUESTION_DUPLICATE_STATES, self.data_ingestor).func()
        expected = {'Washington': 27.7, 'Arkansas': 27.8, 'Massachusetts': 29.3, 'Ohio': 29.4, 'Louisiana': 30.0}
        self.assertEqual(actual, expected)

    def test_best5_max_is_best(self):
        actual = task.TaskBest5(0, QUESTION_UNIQUE_STATES, self.data_ingestor).func()
        expected = {'Vermont': 37.9, 'Michigan': 33.1, 'Oregon': 30.9, 'Tennessee': 30.9, 'Connecticut': 29.3}
        self.assertEqual(actual, expected)

    def test_diff_from_mean_duplicate_states(self):
        actual = task.TaskDiffFromMean(0, QUESTION_DUPLICATE_STATES, self.data_ingestor).func()
        expected = {'Arkansas': 3.3, 'Indiana': -13.0, 'Louisiana': 1.1,
                    'Massachusetts': 1.8, 'New Mexico': 0.6, 'Ohio': 1.7, 'Washington': 3.4}
        self.__assert_dicts_with_tolerance(actual, expected)
        
    def test_diff_from_mean_unique_states(self):
        actual = task.TaskDiffFromMean(0, QUESTION_UNIQUE_STATES, self.data_ingestor).func()
        expected = {'Connecticut': 0.2, 'Louisiana': 5.6, 'Michigan': -3.6, 
                    'Missouri': 9.0, 'Oregon': -1.4, 'Tennessee': -1.4, 'Vermont': -8.4}
        self.__assert_dicts_with_tolerance(actual, expected)

    def test_global_mean_duplicate_states(self):
        actual = task.TaskGlobalMean(0, QUESTION_DUPLICATE_STATES, self.data_ingestor).func()
        expected = {'global_mean' : 31.1}
        self.__assert_dicts_with_tolerance(actual, expected)
    
    def test_global_mean_unique_states(self):
        actual = task.TaskGlobalMean(0, QUESTION_UNIQUE_STATES, self.data_ingestor).func()
        expected = {'global_mean' : 29.5}
        self.__assert_dicts_with_tolerance(actual, expected)
    
    def test_mean_by_category(self):
        actual = task.TaskMeanByCategory(0, QUESTION_DUPLICATE_STATES, self.data_ingestor).func()
        expected = {"('Arkansas', 'Income', '$25,000 - $34,999')": 27.8,
                    "('Indiana', 'Race/Ethnicity', 'Non-Hispanic Black')": 44.1,
                    "('Louisiana', 'Education', 'College graduate')": 27.5,
                    "('Louisiana', 'Education', 'Less than high school')": 32.5,
                    "('Massachusetts', 'Income', '$50,000 - $74,999')": 29.3,
                    "('New Mexico', 'Income', 'less than $25,000')": 30.5,
                    "('Ohio', 'Income', '$75,000 or greater')": 29.4,
                    "('Washington', 'Gender', 'Female')": 27.7}
        self.assertEqual(actual, expected)

    def test_state_diff_from_mean_duplicate_states(self):
        actual = task.TaskStateDiffFromMean(0, QUESTION_DUPLICATE_STATES, self.data_ingestor, "Louisiana").func()
        expected = {'Louisiana' : 1.1}
        self.__assert_dicts_with_tolerance(actual, expected)
    
    def test_state_diff_from_mean_unique_states(self):
        actual = task.TaskStateDiffFromMean(0, QUESTION_UNIQUE_STATES, self.data_ingestor, 'Vermont').func()
        expected = {'Vermont' : -8.4}
        self.__assert_dicts_with_tolerance(actual, expected)

    def test_state_mean(self):
        actual = task.TaskStateMean(0, QUESTION_DUPLICATE_STATES, self.data_ingestor, 'Louisiana').func()
        expected = {'Louisiana' : 30.0}
        self.assertEqual(actual, expected)

    def test_states_mean(self):
        actual = task.TaskStatesMean(0, QUESTION_DUPLICATE_STATES, self.data_ingestor).func()
        expected = {'Washington': 27.7, 'Arkansas': 27.8, 'Massachusetts': 29.3, 'Ohio': 29.4,
                    'Louisiana': 30.0, 'Indiana': 44.1, 'New Mexico': 30.5}
        self.__assert_dicts_with_tolerance(actual, expected)
    
    def test_state_mean_by_category_duplicate_states(self):
        actual = task.TaskStateMeanByCategory(0, QUESTION_DUPLICATE_STATES, self.data_ingestor, 'Louisiana').func()
        expected = {'Louisiana' :{"('Education', 'College graduate')": 27.5,
                    "('Education', 'Less than high school')": 32.5,}}
        self.assertEqual(actual, expected)
    
    def test_state_mean_by_category_unique_states(self):
        actual = task.TaskStateMeanByCategory(0, QUESTION_UNIQUE_STATES, self.data_ingestor, 'Vermont').func()
        expected = {'Vermont': {"('Education', 'Less than high school')": 37.9}}
        self.assertEqual(actual, expected)

    def test_worst5_best_is_min(self):
        actual = task.TaskWorst5(0, QUESTION_DUPLICATE_STATES, self.data_ingestor).func()
        expected = {'Indiana': 44.1, 'New Mexico': 30.5, 'Louisiana':30.0, 'Ohio': 29.4, 'Massachusetts': 29.3}
        self.assertEqual(actual, expected)

    def test_worst5_best_is_max(self):
        actual = task.TaskWorst5(0, QUESTION_UNIQUE_STATES, self.data_ingestor).func()
        expected = {'Missouri': 20.5, 'Louisiana': 23.9, 'Connecticut': 29.3, 'Oregon': 30.9, 'Tennessee': 30.9}
        self.assertEqual(actual, expected)
