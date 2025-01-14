

from airflow.models import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from random import randint
from datetime import datetime, timedelta
import time

# This function pulls data from XCom
def _choose_best_model(ti):

    # XCom is being used here to pull the accuracies from the previous tasks
    accuracies = ti.xcom_pull(task_ids=[
        'training_model_A',
        'training_model_B',
        'training_model_C'
    ])
    if not all(accuracies):
        raise ValueError("One or more models did not return a valid accuracy.")
    best_accuracy = max(accuracies)
    if best_accuracy > 8:
        return 'accurate'
    return 'inaccurate'

def _training_model():
    return randint(1, 10)

def delay_task():
    time.sleep(300)  # Delays the task by 300 seconds
    return _training_model()  # Call the model training function

def delay_taskVersion2():
    time.sleep(600)  # Delays the task by 300 seconds
    return _training_model()  # Call the model training function



default_args = {
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG("my_dag", default_args=default_args, start_date=datetime(2025, 1, 1), schedule_interval="@daily", catchup=False) as dag:

    # These PythonOperator tasks push their return values to XCom
    training_model_A = PythonOperator(
        task_id="training_model_A",
        python_callable=_training_model
    )

    training_model_B = PythonOperator(
        task_id="training_model_B",
        python_callable=_training_model
    )

    training_model_C = PythonOperator(
        task_id="training_model_C",
        python_callable=_training_model
        #python_callable=_training_model
    )

    # This BranchPythonOperator task pulls data from XCom
    choose_best_model = BranchPythonOperator(
        task_id="choose_best_model",
        python_callable=_choose_best_model
    )

    accurate = BashOperator(
        task_id="accurate",
        bash_command="echo 'accurate'"
    )

    inaccurate = BashOperator(
        task_id="inaccurate",
        bash_command="echo 'inaccurate'"
    )

    # Task dependencies
    [training_model_A, training_model_B, training_model_C] >> choose_best_model >> [accurate, inaccurate]
