import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import pandas as pd
import numpy as np
from dataclasses import dataclass
from sklearn.model_selection import train_test_split
from pathlib import Path
from source.logger.logger import logging    
from source.exception.exception import customexception

@dataclass
class DataIngestionConfig:
    raw_data_path:str=os.path.join("artifacts","raw.csv")
    train_data_path:str=os.path.join("artifacts","train.csv")
    test_data_path:str=os.path.join("artifacts","test.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()
       
    def initiate_data_ingestion(self):
        logging.info("data ingestion started")
        print("adding changes")
        try:
            logging.info(" Reading dataset")
            data= pd.read_csv("https://raw.githubusercontent.com/ravi0dubey/DataSets/refs/heads/main/gemstone.csv")
            os.makedirs(os.path.dirname(os.path.join(self.ingestion_config.raw_data_path)),exist_ok=True)
            data.to_csv(self.ingestion_config.raw_data_path,index=False)
            logging.info("Raw Dataset stored in Artifact folder")
            logging.info("Starting Train Test split")
            train_data,test_data=train_test_split(data,test_size=0.25)
            logging.info("Train Test Split completed")          
            train_data.to_csv(self.ingestion_config.train_data_path,index=False)
            test_data.to_csv(self.ingestion_config.test_data_path,index=False)
            logging.info("Data Ingestion completed")         
            return (self.ingestion_config.train_data_path,self.ingestion_config.test_data_path)
        except Exception as e:
            logging.info()
            raise customexception(e,sys)
# added


if __name__=="__main__":
    obj=DataIngestion()
    train_path, test_path = obj.initiate_data_ingestion()
    print(train_path)
    print(test_path)