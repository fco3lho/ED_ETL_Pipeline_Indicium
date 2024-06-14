from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,  
}

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

  run_first_step >> run_second_step