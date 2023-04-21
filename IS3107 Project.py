import os

from datetime import datetime, timedelta, date
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 4, 15)
}

datetime_today = str(date.today())

processed_title = "Processed-" + str(datetime_today)

def process_cna():
    os.chdir("/home/jacqy/IS3107_25-main/data_processing")
    import processing
    os.chdir(f"/home/jacqy/IS3107_25-main/data_collection/data_collection/spiders/data/{datetime_today}")
    processing.filter_title('cna.json')

def process_krasia():
    os.chdir("/home/jacqy/IS3107_25-main/data_processing")
    import processing
    os.chdir(f"/home/jacqy/IS3107_25-main/data_collection/data_collection/spiders/data/{datetime_today}")
    processing.filter_title('krasia.json')

def process_today():
    os.chdir("/home/jacqy/IS3107_25-main/data_processing")
    import processing
    os.chdir(f"/home/jacqy/IS3107_25-main/data_collection/data_collection/spiders/data/{datetime_today}")
    processing.filter_title('today.json')

def load_data():
    pass




with DAG(
    'IS3107_Project_Tester',
    default_args=default_args,
    description='DAG for running Scrapy spiders',
    schedule_interval=timedelta(days=1),
) as dag:
    
    dag.doc_md = __doc__

    extract_data_cna = BashOperator(
        task_id='extract_data_cna',
        bash_command=f"cd ~ && cd IS3107_25-main/data_collection/data_collection/spiders && scrapy crawl cna -o data/{datetime_today}/cna.json"
    )

    extract_data_krasia = BashOperator(
        task_id='extract_data_krasia',
        bash_command=f"cd ~ && cd IS3107_25-main/data_collection/data_collection/spiders && scrapy crawl krasia -o data/{datetime_today}/krasia.json"
    )

    extract_data_today = BashOperator(
        task_id='extract_data_today',
        bash_command=f"cd ~ && cd IS3107_25-main/data_collection/data_collection/spiders && scrapy crawl today -o data/{datetime_today}/today.json"
    )

    process_data_cna = PythonOperator(
        task_id='process_data_cna',
        python_callable=process_cna,
    )

    process_data_krasia = PythonOperator(
        task_id='process_data_krasia',
        python_callable=process_krasia,
    )

    process_data_today = PythonOperator(
        task_id='process_data_today',
        python_callable=process_today,
    )

    extract_data_cna >> process_data_cna
    extract_data_krasia >> process_data_krasia
    extract_data_today >> process_data_today
