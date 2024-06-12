from datetime import datetime
import subprocess
from airflow import DAG
from airflow.operators.python import PythonOperator

def meltano_script():
  path = "../../first_step/script.py"
  result = subprocess.run(['python', path], capture_output=True, text=True)
  print("Output:")
  print(result.stdout)
  print("Errors:")
  print(result.stderr)

with DAG ('indicium_dag', start_date = datetime(2024,6,11), schedule_interval = '@daily', catchup = False) as dag:
  meltano_script = PythonOperator(
    task_id = "meltano_script",
    python_callable = meltano_script
  )