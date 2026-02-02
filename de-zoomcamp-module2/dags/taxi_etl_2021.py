import os
import gzip
import logging
import requests
import pendulum
import pandas as pd
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

# --- Configuration ---
LOCAL_TZ = pendulum.timezone("America/New_York")
DATA_DIR = os.environ.get("AIRFLOW_HOME", "/opt/airflow") + "/data"
BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/"

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def download_taxi_data(taxi_type: str, year: int, month: int):
    """Downloads the .csv.gz file for a specific taxi, year, and month."""
    file_name = f"{taxi_type}_tripdata_{year}-{month:02d}.csv.gz"
    url = f"{BASE_URL}{taxi_type}/{file_name}"
    local_path = os.path.join(DATA_DIR, file_name)

    logging.info(f"Downloading {file_name} from {url}")
    
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(local_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                f.write(chunk)
        logging.info(f"Successfully downloaded {file_name} to {local_path}")
        return local_path
    else:
        raise Exception(f"Failed to download {file_name}. Status code: {response.status_code}")

def process_taxi_data(taxi_type: str, year: int, month: int, **kwargs):
    """Decompresses the file, logs size, and counts rows."""
    ti = kwargs['ti']
    # If using dynamic task mapping or complex dependencies, you might get path from xcom
    # But for a simple loop DAG, we can reconstruct or pass it
    file_name = f"{taxi_type}_tripdata_{year}-{month:02d}.csv.gz"
    local_path = os.path.join(DATA_DIR, file_name)
    
    if not os.path.exists(local_path):
        raise FileNotFoundError(f"Compressed file {local_path} not found.")

    # Get compressed size
    compressed_size = os.path.getsize(local_path) / (1024 * 1024)
    logging.info(f"Compressed file size: {compressed_size:.2f} MB")

    # Unzip and process
    csv_file_name = file_name.replace(".gz", "")
    csv_path = os.path.join(DATA_DIR, csv_file_name)

    logging.info(f"Decompressing {file_name} to {csv_path}")
    
    with gzip.open(local_path, 'rb') as f_in:
        with open(csv_path, 'wb') as f_out:
            f_out.write(f_in.read())
    
    # Get uncompressed size
    uncompressed_size = os.path.getsize(csv_path) / (1024 * 1024)
    logging.info(f"Uncompressed file size: {uncompressed_size:.2f} MB")

    # Count rows using pandas
    try:
        df = pd.read_csv(csv_path, low_memory=False)
        row_count = len(df)
        logging.info(f"Processed {csv_file_name}: {row_count} rows found.")
    except Exception as e:
        logging.error(f"Error reading CSV {csv_file_name}: {e}")
        # Fallback to simple line count if pandas fails due to memory/types
        with open(csv_path, 'r') as f:
            row_count = sum(1 for line in f) - 1 # Subtract header
        logging.info(f"Row count (fallback): {row_count}")

# --- DAG Definition ---
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1, tzinfo=LOCAL_TZ),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

with DAG(
    'nyc_taxi_etl_2021',
    default_args=default_args,
    description='ETL for NYC Taxi data (2019-2021)',
    schedule_interval=None,  # Manual trigger / Backfill
    catchup=False,
    tags=['zoomcamp', 'homework'],
) as dag:

    for taxi in ["yellow", "green"]:
        with TaskGroup(group_id=f"{taxi}_tasks") as taxi_group:
            
            # Loop through years and months
            periods = []
            for year in [2019, 2020]:
                for month in range(1, 13):
                    periods.append((year, month))
            # 2021 focus (Jan to Jul)
            for month in range(1, 8):
                periods.append((2021, month))

            for year, month in periods:
                task_id_suffix = f"{year}_{month:02d}"
                
                download_task = PythonOperator(
                    task_id=f"download_{taxi}_{task_id_suffix}",
                    python_callable=download_taxi_data,
                    op_kwargs={'taxi_type': taxi, 'year': year, 'month': month},
                )

                process_task = PythonOperator(
                    task_id=f"process_{taxi}_{task_id_suffix}",
                    python_callable=process_taxi_data,
                    op_kwargs={'taxi_type': taxi, 'year': year, 'month': month},
                    provide_context=True,
                )

                download_task >> process_task
