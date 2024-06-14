from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
import json
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,  
}

def generate_success_json():
   success_info = {
      "status": "Success when running DAG!",
      "date": f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
   }

   home_directory = os.path.expanduser('~')
   file_path = os.path.join(home_directory, f"indicium-test/messages/{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}_success.json")

   out_file = open(file_path, "w") 
   json.dump(success_info, out_file, indent = 4) 
   out_file.close() 

with DAG ('indicium_dag', 
          description='DAG to run Meltano steps sequentially',
          default_args=default_args,
          start_date = days_ago(1), 
          schedule_interval = "@daily", 
          catchup = False) as dag:
  
   run_first_step = BashOperator(
     task_id = "run_first_step",
     bash_command = "~/indicium-test/run_first_step.sh ~/indicium-test/first_step"
   )

   run_second_step = BashOperator(
     task_id = "run_second_step",
     bash_command = "~/indicium-test/run_second_step.sh ~/indicium-test/second_step"
   )

   generate_success_file = PythonOperator(
      task_id = "generate_success_json",
      python_callable = generate_success_json
   )

run_first_step >> run_second_step >> generate_success_file