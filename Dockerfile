FROM apache/airflow:latest

RUN pip install apache-airflow-providers-docker
COPY airflow/airflow.cfg /opt/airflow/


