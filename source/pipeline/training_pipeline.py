import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from source.logger.logger import logging
from source.exception.exception import customexception
import pandas as pd
from source.components.data_ingestion import DataIngestion
from source.components.data_transformation import DataTransformation
from source.components.model_trainer import ModelTrainer
from source.components.model_evaluation import ModelEvaluation

class Training_Pipeline:
    def start_data_ingestion(self):
        try:
            data_ingestion_obj=DataIngestion()
            train_data_path,test_data_path=data_ingestion_obj.initiate_data_ingestion()
            return train_data_path,test_data_path
        except Exception as e:
            raise customexception(e)
    
    def start_data_transformation(self,train_data_path,test_data_path):
        try:
            data_transformation=DataTransformation()
            train_arr_path,test_arr_path=data_transformation.initialize_data_transformation(train_data_path,test_data_path)
            return train_arr_path,test_arr_path
        except Exception as e:
            raise customexception(e)

    def start_model_training(self,train_arr_path,test_arr_path):
        try:
            model_trainer_obj=ModelTrainer()
            model_trainer_obj.initate_model_training(train_arr_path,test_arr_path)
            return model_trainer_obj
        except Exception as e:
            raise customexception(e)
        
    def start_model_evaluation(self,train_arr_path,test_arr_path):
        try:
            model_eval_obj = ModelEvaluation()
            model_eval_obj.initiate_model_evaluation(train_arr_path,test_arr_path)
        except Exception as e:
            raise customexception(e)
        
    def start_training_pipeline(self):
        train_data_path,test_data_path= self.start_data_ingestion()
        train_arr_path,test_arr_path= self.start_data_transformation(train_data_path,test_data_path)
        self.start_model_training(train_arr_path,test_arr_path)
        self.start_model_evaluation(train_arr_path,test_arr_path)

if __name__=="__main__":
    training_object = Training_Pipeline()
    training_object.start_training_pipeline()
