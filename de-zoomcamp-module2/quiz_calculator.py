import os
import gzip
import requests
import pandas as pd
import logging

DATA_DIR = "./data"
BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/"

logging.basicConfig(level=logging.INFO, format='%(message)s')

def download_and_decompress(taxi_type, year, month):
    file_name = f"{taxi_type}_tripdata_{year}-{month:02d}.csv.gz"
    url = f"{BASE_URL}{taxi_type}/{file_name}"
    local_gz = os.path.join(DATA_DIR, file_name)
    local_csv = local_gz.replace(".gz", "")

    if os.path.exists(local_csv):
        return local_csv

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    logging.info(f"Downloading {file_name}...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(local_gz, "wb") as f:
            f.write(response.content)
        
        logging.info(f"Decompressing {file_name}...")
        with gzip.open(local_gz, 'rb') as f_in:
            with open(local_csv, 'wb') as f_out:
                f_out.write(f_in.read())
        
        # Cleanup gz to save space
        os.remove(local_gz)
        return local_csv
    else:
        logging.error(f"Failed to download {file_name}")
        return None

def answer_quiz():
    logging.info("--- Data Science Quiz Calculator ---")
    
    # Q1: yellow_tripdata_2020-12.csv size
    logging.info("\nChecking Q1: Yellow Taxi 2020-12 size...")
    file_2020_12 = download_and_decompress("yellow", 2020, 12)
    if file_2020_12:
        size_bytes = os.path.getsize(file_2020_12)
        size_mib = size_bytes / (1024 * 1024)
        logging.info(f"Q1 Results: {size_mib:.1f} MiB")

    # Q3: Yellow Taxi 2020 total rows
    logging.info("\nChecking Q3: Yellow Taxi 2020 total rows...")
    yellow_2020_total = 0
    for m in range(1, 13):
        csv_file = download_and_decompress("yellow", 2020, m)
        if csv_file:
            df = pd.read_csv(csv_file, low_memory=False)
            yellow_2020_total += len(df)
    logging.info(f"Q3 Results: {yellow_2020_total:,}")

    # Q4: Green Taxi 2020 total rows
    logging.info("\nChecking Q4: Green Taxi 2020 total rows...")
    green_2020_total = 0
    for m in range(1, 13):
        csv_file = download_and_decompress("green", 2020, m)
        if csv_file:
            df = pd.read_csv(csv_file, low_memory=False)
            green_2020_total += len(df)
    logging.info(f"Q4 Results: {green_2020_total:,}")

    # Q5: Yellow Taxi 2021-03 row count
    logging.info("\nChecking Q5: Yellow Taxi 2021-03 row count...")
    file_2021_03 = download_and_decompress("yellow", 2021, 3)
    if file_2021_03:
        df = pd.read_csv(file_2021_03, low_memory=False)
        logging.info(f"Q5 Results: {len(df):,}")

if __name__ == "__main__":
    answer_quiz()
