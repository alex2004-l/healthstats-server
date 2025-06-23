import pandas as pd


class DataIngestor:
    QUESTION = "Question"
    STATE = "LocationDesc"
    VALUE = "Data_Value"
    STRATIFICATION = "Stratification1"
    CATEGORY = "StratificationCategory1"
    COLUMNS = [QUESTION, STATE, VALUE, STRATIFICATION, CATEGORY]

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
        '''Private method for filtering frame by question'''
        return self.database_df[self.database_df[self.QUESTION] == question]

    def __get_df_by_question_and_state(self, question : str, state : str) -> pd.DataFrame:
        '''Private method for filtering frame by question and state'''
        df_by_question = self.__get_df_by_question(question)
        return df_by_question[df_by_question[self.STATE] == state]

    def get_mean_values_for_all_states(self, question : str) -> dict:
        '''Method for calculating mean values for all states from database'''
        df = self.__get_df_by_question(question)
        return df.groupby(self.STATE)[self.VALUE].mean().to_dict()

    def get_mean_value_for_state(self, question : str, state : str) -> dict:
        '''Method for calculating the mean value for a state from database'''
        df = self.__get_df_by_question_and_state(question, state)
        result = df[self.VALUE].mean()
        return {state : result}

    def check_question_best_is_min(self, question : str) -> bool:
        '''Checks if a function is in best_is_min question set'''
        return question in self.questions_best_is_min

    def check_question_worst_is_min(self, question : str) -> bool:
        '''Checks if a function is in best_is_max question set'''
        return question in self.questions_best_is_max

    def get_global_mean(self, question : str) -> float:
        '''Calculates the global mean of a question'''
        df = self.__get_df_by_question(question)
        return df[self.VALUE].mean()

    def __get_mean_stratification_by_state(self, question : str, state : str) -> dict:
        '''Helper function for calculating the stratification by state'''
        df = self.__get_df_by_question_and_state(question, state)
        return df.groupby([self.CATEGORY, self.STRATIFICATION])[self.VALUE].mean().to_dict()

    def get_mean_stratification(self, question : str) -> dict:
        '''Function that calculates the stratification for all states'''
        df = self.__get_df_by_question(question)
        # Groups the df rows by state, stratification and category and calculates the mean valoe
        return df.groupby([self.STATE, self.CATEGORY, self.STRATIFICATION])[self.VALUE].mean().to_dict()

    def get_mean_stratification_state(self, question : str, state : str) -> dict:
        '''Returns the stratification by state in the right format'''
        return {state : self.__get_mean_stratification_by_state(question, state)}
