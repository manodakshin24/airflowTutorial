# airflowTutorial
Airflow tutorial showcasing a custom DAG with XCom for inter-task communication:

This guide will show you how to set up Apache Airflow, run a simple DAG (my_dag), and monitor its execution. Perfect for data engineering freshers who want to learn Airflow!

Prerequisites:

-> Python 3.6+
-> Pip (Python package installer)
Make sure these are installed before proceeding.

Installing Apache Airflow
Create a virtual environment (optional but recommended):

python3 -m venv airflow_venv
source airflow_venv/bin/activate  # On Windows, use `airflow_venv\Scripts\activate`

Install Apache Airflow:
pip install apache-airflow
If you need a specific version, use version 2.6.0+

Set Up Airflow
Initialize the Airflow database:
airflow db init


Start the Airflow web server:
airflow webserver --port 8080

Access the UI at http://localhost:8080.

Start the scheduler:
airflow scheduler

Alternatively, you can also use airflow standalone to initialize the database, create a user, and start all components.

Understanding the DAG

The DAG in my_dag.py trains three models and chooses the best one based on accuracy. Key tasks:

Model Training: Three tasks simulate training models by generating random accuracy scores.
Model Selection: A task evaluates the best model using the BranchPythonOperator.