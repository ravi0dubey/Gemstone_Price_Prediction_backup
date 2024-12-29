from __future__ import annotations
from asyncio import tasks
import json
from textwrap import dedent
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from source.pipeline.training_pipeline import Training_Pipeline
import pendulum

training_pipeline = Training_Pipeline()

with DAG(
    'Gemstone_training',
    default_args={'retries': 2},
    description='Gemstone Prediction',
    schedule_interval="@weekly",
    start_date=pendulum.datetime(2024, 12, 29, tz="UTC"),
    catchup=False,
    tags=['machine learning',"gemstone"],
) as dag:

    dag.doc_md = __doc__

    def data_ingestion(**kwargs):
        ti = kwargs["ti"]
        train_data_path,test_data_path=training_pipeline.start_data_ingestion()
        ti.xcom_push("data_ingestion_artifact",{"train_data_path":train_data_path},{"test_data_path" : test_data_path})
    
    def data_transformation(**kwargs):
        ti = kwargs["ti"]
        train_data_path,test_data_path=ti.xcom_pull(task_ids="data_ingestion")
        train_arr_path,test_arr_path=training_pipeline.start_data_transformation(train_data_path,test_data_path)
        ti.xcom_push("data_transformation_artifact",{"train_arr_path":train_arr_path},{"test_arr_path" : test_arr_path})
                          
    def model_training(**kwargs):
        ti = kwargs["ti"]
        train_arr_path,test_arr_path=ti.xcom_pull(task_ids="data_transformation")
        training_pipeline.start_model_training(train_arr_path,test_arr_path)

    def model_evaluation(**kwargs):
        ti = kwargs["ti"]
        train_arr_path,test_arr_path=ti.xcom_pull(task_ids="data_transformation")
        training_pipeline.start_model_evaluation(train_arr_path,test_arr_path)
    
    data_ingestion_pipeline  = PythonOperator(
            task_id="data_ingestion",
            python_callable=data_ingestion
    )
    
    data_transformation_pipeline  = PythonOperator(
            task_id="data_transformation",
            python_callable=data_ingestion
    )
    
    model_training_pipeline  = PythonOperator(
            task_id="model_training",
            python_callable=model_training
    )

    model_evaluation_pipeline  = PythonOperator(
            task_id="model_evaluation",
            python_callable=model_training
    )

    data_ingestion_pipeline>>data_transformation_pipeline>>training_pipeline>>model_evaluation_pipeline