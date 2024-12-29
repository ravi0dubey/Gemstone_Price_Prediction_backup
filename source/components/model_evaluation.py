import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import mlflow
import numpy as np
import pickle
import distutils

from source.utils.utils import load_object,load_numpy_array_data
from urllib.parse import urlparse
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
from source.logger.logger import logging
from source.exception. exception import customexception

class ModelEvaluation:
    def __init__(self):
        logging.info("evaluation started")

    def eval_metrics(self,actual,pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        logging.info("evaluation metrics captured")
        return rmse, mae, r2
# added
    def initiate_model_evaluation(self,train_array_path,test_array_path):
        try:
            print(distutils.__file__)
            train_arr = load_numpy_array_data(train_array_path)
            test_arr = load_numpy_array_data(test_array_path)
            X_train, y_train, X_test, y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1])
            model_path=os.path.join("artifacts","model.pkl")
            model=load_object(model_path)
            train_npy_path=os.path.join("artifacts","train.npy")
            train_npy=load_numpy_array_data(train_npy_path)
            mlflow.set_tracking_uri(uri="http://127.0.0.1:7071")     
            mlflow.set_registry_uri("")     
            logging.info("model has register")
            tracking_url_type_store=urlparse(mlflow.get_tracking_uri()).scheme
            print(tracking_url_type_store)
            with mlflow.start_run():
                prediction=model.predict(X_test)
                (rmse,mae,r2)=self.eval_metrics(y_test,prediction)
                mlflow.log_metric("rmse", rmse)
                mlflow.log_metric("r2", r2)
                mlflow.log_metric("mae", mae)
                 # Model registry does not work with file store
                if tracking_url_type_store != "file":
                    # https://mlflow.org/docs/latest/model-registry.html#api-workflow
                    mlflow.sklearn.log_model(model, "model", registered_model_name="ml_modelRAVI")
                    mlflow.log_artifacts("artifacts")
                else:
                    mlflow.sklearn.log_model(model, "model")
                    mlflow.sklearn.log_model(model, "model", registered_model_name="ml_modelRAVI")
                    mlflow.log_artifacts("artifacts")
        except Exception as e:
            raise customexception(e,sys)
        

if __name__=="__main__":
    model_trainer_obj=ModelEvaluation()
    model_trainer_obj.initiate_model_evaluation('artifacts/train.npy','artifacts/test.npy')      