import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import pandas as pd
import numpy as np
from dataclasses import dataclass
from pathlib import Path
from source.logger.logger import logging
from source.exception.exception import customexception
from source.utils.utils import save_object,evaluate_model,load_numpy_array_data
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression, Ridge,Lasso,ElasticNet
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression,Lasso,Ridge,ElasticNet


@dataclass 
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts','model.pkl')
    
    
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    
    def initate_model_training(self,train_array_path,test_array_path):
        try:
            logging.info('Splitting Dependent and Independent variables from train and test data')
            #loading training array and testing array
            train_arr = load_numpy_array_data(train_array_path)
            test_arr = load_numpy_array_data(test_array_path)
            X_train, y_train, X_test, y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            models={
            'LinearRegression':LinearRegression(),
            'Lasso':Lasso(),
            'Ridge':Ridge(),
            'Elasticnet':ElasticNet(),
            'Randomforest':RandomForestRegressor(),
            'xgboost':XGBRegressor()
        }
            
            model_report:dict=evaluate_model(X_train,y_train,X_test,y_test,models)
            print(model_report)
            logging.info(f'Model Report : {model_report}')

            # To get best model score from dictionary 
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            
            best_model = models[best_model_name]
            print(f'Best Model Found , Model Name : {best_model_name} , R2 Score : {best_model_score}')
            print('\n====================================================================================\n')
            logging.info(f'Best Model Found , Model Name : {best_model_name} , R2 Score : {best_model_score}')
            save_object(
                 file_path=self.model_trainer_config.trained_model_file_path,
                 obj=best_model
            )
          
        except Exception as e:
            logging.info('Exception occured at Model Training')
            raise customexception(e,sys)

# added
if __name__=="__main__":
    model_trainer_obj=ModelTrainer()
    model_trainer_obj.initate_model_training('artifacts/train.npy','artifacts/test.npy')      
    