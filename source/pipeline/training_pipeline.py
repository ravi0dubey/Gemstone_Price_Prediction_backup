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

def start_training_pipeline():
    obj=DataIngestion()
    train_data_path,test_data_path=obj.initiate_data_ingestion()
    data_transformation=DataTransformation()
    train_arr,test_arr=data_transformation.initialize_data_transformation(train_data_path,test_data_path)

    model_trainer_obj=ModelTrainer()
    model_trainer_obj.initate_model_training(train_arr,test_arr)
    # added
    model_eval_obj = ModelEvaluation()
    model_eval_obj.initiate_model_evaluation(train_arr,test_arr)

if __name__=="__main__":
    start_training_pipeline()