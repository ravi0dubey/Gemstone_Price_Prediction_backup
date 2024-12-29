from __future__ import annotations
from asyncio import tasks
import json
from textwrap import dedent
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from source.pipeline.training_pipeline import start_training_pipeline
import pendulum


with DAG(
    'Gemstone_training',
    default_args={'retries': 2},
    description='Gemstone Prediction',
    schedule_interval="@weekly",
    start_date=pendulum.datetime(2022, 12, 11, tz="UTC"),
    catchup=False,
    tags=['example'],
) as dag:

    
    def training(**kwargs):
        
        start_training_pipeline()
    

    training_pipeline  = PythonOperator(
            task_id="train_pipeline",
            python_callable=training
    )

    training_pipeline