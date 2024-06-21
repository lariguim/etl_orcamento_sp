#!/usr/bin/env bash

export PYTHONPATH=$(pwd)/scripts:$(pwd)/dags:$PYTHONPATH


airflow db init

airflow users create \
    --username admin \
    --firstname Admin \
    --lastname Admin \
    --role Admin \
    --password admin \
    

airflow scheduler & airflow webserver
