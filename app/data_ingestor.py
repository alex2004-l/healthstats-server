import json
import pandas as pd

class DataIngestor:
    QUESTION = "Question"
    STATE = "LocationDesc"
    VALUE = "Data_Value"
    COLUMNS = [QUESTION, STATE, "Data_Value", "Stratification1", "StratificationCategory1"]

    def __init__(self, csv_path: str):
        self.database_df = pd.read_csv(csv_path, usecols=self.COLUMNS)

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
        ]

    def __get_df_by_question(self, question : str) -> pd.DataFrame:
        return self.database_df[self.database_df[self.QUESTION] == question]

    def __get_df_by_question_and_state(self, question : str, state : str) -> pd.DataFrame:
        df_by_question = self.__get_df_by_question(question)
        return df_by_question[df_by_question[self.STATE] == state]
    
    def get_mean_values_for_all_states(self, question : str) -> dict:
        df = self.__get_df_by_question(question)
        return df.groupby(self.STATE)[self.VALUE].mean().to_dict()
    
    def get_mean_value_for_state(self, question : str, state : str) -> dict:
        df = self.__get_df_by_question_and_state(question, state)
        result = df["Data_Value"].mean()
        return {state : result}
    
    def check_question_best_is_min(self, question : str) -> bool:
        return question in self.questions_best_is_min
    
    def check_question_worst_is_min(self, question : str) -> bool:
        return question in self.questions_best_is_max
    
    def get_global_mean(self, question : str) -> float:
        df = self.__get_df_by_question(question)
        return df[self.VALUE].mean()
