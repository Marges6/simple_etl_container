from datetime import datetime, timedelta
from airflow import DAG
import subprocess
from docker.types import Mount
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator

default_args = {
  'owner': 'airflow',
  'depends_on_past': False,
  'email_on_failure': False,
  'email_on_retry': False,
  # 'retries':5,
  # 'retry_delay':timedelta.min(2)
}

def run_etl_script():
  script_path = "/opt/airflow/etl_script/scripts/etl_script.py"
  result = subprocess.run(["python",script_path],
                          capture_output=True, text=True)
  if result.returncode != 0:
    raise Exception(f"Script failed with error: {result.stderr}")
  else:
    print(result.stdout)

dag = DAG(
  'simple_etl',
  default_args=default_args,
  description='ETL workflow',
  start_date=datetime(2024,3,24),
  schedule_interval='@daily',
  #catchup=False
)

t1 = PythonOperator(
  task_id="run_etl_script",
  python_callable=run_etl_script,
  dag=dag
)

# t2 = DockerOperator(
#   task_id="run generator"
#   image=''
#   command=[

#   ]
#   auto_remove=True,
#   docker_url="unix://var/run/docker.sock",
#   network_mode="bridge",
#   mounts=[
#     Mount(source='',
#           target='',type='bind')],
#   dag=dag
# )


# t3 >> t2 >> t1
