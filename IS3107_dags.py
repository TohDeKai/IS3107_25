import os
import sys

from datetime import datetime, timedelta, date
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

import processing

from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 4, 15)
}

datetime_today = str(date.today())

processed_title = "Processed-" + str(datetime_today)
sys.path.insert(0,os.path.abspath(os.path.dirname(__file__)))

def process_cna():
    print("*****")
    os.chdir("/Users/tohdekai/IS3107_25/data_processing")
    import nltk
    import processing
    os.chdir(f"/Users/tohdekai/IS3107_25/data_collection/data_collection/spiders/data/{datetime_today}")
    export = processing.export('cna.json')
    jsonFile = open("cleaned_news.json", "a")
    jsonFile.write(export)
    jsonFile.close()

    
def process_krasia():
    os.chdir("/Users/tohdekai/IS3107_25/data_processing")
    import nltk
    import processing
    os.chdir(f"/Users/tohdekai/IS3107_25/data_collection/data_collection/spiders/data/{datetime_today}")
    export = processing.export('krasia.json')
    jsonFile = open("cleaned_news.json", "a")
    jsonFile.write(export)
    jsonFile.close()

def process_today():
    os.chdir("/Users/tohdekai/IS3107_25/data_processing")
    import nltk
    import processing
    os.chdir(f"/Users/tohdekai/IS3107_25/data_collection/data_collection/spiders/data/{datetime_today}")
    export = processing.export('today.json')
    jsonFile = open("cleaned_news.json", "a")
    jsonFile.write(export)
    jsonFile.close()

def process_asean():
    os.chdir("/Users/tohdekai/IS3107_25/data_processing")
    import nltk
    import processing
    os.chdir(f"/Users/tohdekai/IS3107_25/data_collection/data_collection/spiders/data/{datetime_today}")
    export = processing.export('asean.json')
    jsonFile = open("cleaned_news.json", "a")
    jsonFile.write(export)
    jsonFile.close()

def process_bbc():
    os.chdir("/Users/tohdekai/IS3107_25/data_processing")
    import nltk
    import processing
    os.chdir(f"/Users/tohdekai/IS3107_25/data_collection/data_collection/spiders/data/{datetime_today}")
    export = processing.export('bbc.json')
    jsonFile = open("cleaned_news.json", "a")
    jsonFile.write(export)
    jsonFile.close()

def upload_data():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/tohdekai/IS3107_25/alpine-beacon-384406-a761969b08d8.json" 
    client = storage.Client()
    bucket = client.bucket('is3107_proj')
    blob = bucket.blob('cleaned_news.json')
    os.chdir(f"/Users/tohdekai/IS3107_25/data_collection/data_collection/spiders/data/{datetime_today}")
    blob.upload_from_filename("x.txt")

    
def upload_data_to_bigquery():
    pass

def assign_sentiment():
    pass

with DAG(
    'IS3107_Project_Scrapping_PreProcessing',
    default_args=default_args,
    description='DAG for running Scrapy spiders and preprocessing them',
    schedule_interval=timedelta(days=1),
) as dag:
    
    dag.doc_md = __doc__

    extract_data_cna = BashOperator(
        task_id='extract_data_cna',
        bash_command=f"cd ~ && cd IS3107_25/data_collection/data_collection/spiders && scrapy crawl cna -o data/{datetime_today}/cna.json"
    )

    extract_data_krasia = BashOperator(
        task_id='extract_data_krasia',
        bash_command=f"cd ~ && cd IS3107_25/data_collection/data_collection/spiders && scrapy crawl krasia -o data/{datetime_today}/krasia.json"
    )

    extract_data_today = BashOperator(
        task_id='extract_data_today',
        bash_command=f"cd ~ && cd IS3107_25/data_collection/data_collection/spiders && scrapy crawl today -o data/{datetime_today}/today.json"
    )

    extract_data_asean = BashOperator(
        task_id='extract_data_asean',
        bash_command=f"cd ~ && cd IS3107_25/data_collection/data_collection/spiders && scrapy crawl asean -o data/{datetime_today}/asean.json"
    )

    extract_data_bbc = BashOperator(
        task_id='extract_data_bbc',
        bash_command=f"cd ~ && cd IS3107_25/data_collection/data_collection/spiders && scrapy crawl bbc -o data/{datetime_today}/bbc.json"
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

    process_data_asean = PythonOperator(
        task_id='process_data_asean',
        python_callable=process_asean,
    )

    process_data_bbc = PythonOperator(
        task_id='process_data_bbc',
        python_callable=process_bbc,
    )

    upload_data = PythonOperator(
        task_id='upload_data_to_storage',
        python_callable=upload_data,
    )

    upload_data_bigquery = PythonOperator(
        task_id='upload_data_to_bigquery',
        python_callable=upload_data_to_bigquery,
    )

    assign_sentiment = PythonOperator(
        task_id='assign_sentiment',
        python_callable=assign_sentiment,
    )

    extract_data_cna >> process_data_cna
    extract_data_krasia >> process_data_krasia
    extract_data_today >> process_data_today
    extract_data_asean >> process_data_asean
    extract_data_bbc >> process_data_bbc

    process_data_cna >> upload_data
    process_data_krasia >> upload_data
    process_data_today >> upload_data
    process_data_asean >> upload_data
    process_data_bbc >> upload_data

    upload_data >> upload_data_bigquery >> assign_sentiment