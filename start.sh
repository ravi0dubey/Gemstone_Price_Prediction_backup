#!bin/sh
nohup airflow scheduler &
airflow webserver &
mlflow server --host 0.0.0.0 --port 7071
