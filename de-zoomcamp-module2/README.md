# DE Zoomcamp Module 2 Homework - NYC Taxi ETL with Airflow

This project implements an ETL pipeline using Apache Airflow to process NYC Taxi data (Yellow and Green) for the years 2019, 2020, and 2021 (January to July).

## Project Structure

```text
de-zoomcamp-module2/
├── dags/
│   └── taxi_etl_2021.py    # Main Airflow DAG
├── data/                   # Directory where downloaded data is stored
├── quiz_calculator.py      # Helper script for quiz answers
├── validate_2021_data.py   # Script to verify 2021 data
└── README.md               # This file
```

## Prerequisites

- Apache Airflow 2.x
- Python packages: `pandas`, `requests`

## Airflow DAG: `nyc_taxi_etl_2021`

### Pipeline Steps

1.  **Extract**: Downloads the `.csv.gz` file from the NYC Taxi data GitHub repository.
2.  **Unzip**: Extracts the CSV file from the compressed archive.
3.  **Process/Log**:
    *   Logs the downloaded file name.
    *   Logs the uncompressed file size (in MB).
    *   Counts the number of rows using Pandas (with a fallback to simple line counting).

### Dynamic Task Generation

The DAG dynamically generates tasks for:
- **Taxi Types**: `yellow`, `green`
- **Years**: `2019`, `2020`, `2021`
- **Months**: 01-12 for 2019/2020, 01-07 for 2021.

### How to Run

1.  Place the `taxi_etl_2021.py` file into your Airflow `dags/` folder.
2.  Ensure your Airflow environment can write to the local filesystem (the `data/` directory will be created relative to `AIRFLOW_HOME`).
3.  Trigger the DAG manually from the Airflow UI.
4.  For 2021 backfills, you can trigger individual tasks or use the backfill command if catchup was enabled (note: `catchup` is currently `False` for safety).

## Logging Example

The DAG provides detailed logs for each task:
```text
INFO - Downloading yellow_tripdata_2021-01.csv.gz from ...
INFO - Uncompressed file size: 125.42 MB
INFO - Processed yellow_tripdata_2021-01.csv: 1369765 rows found.
```

## 🎯 Before Submission Checklist

Before submitting your GitHub link, it is highly recommended to:

- [ ] **Capture a screenshot of the Airflow DAG Graph View**: All tasks should be green (Success).
- [ ] **Capture task logs** showing:
    - Uncompressed file size
    - Row counts
- [ ] **Add these screenshots to a `screenshots/` folder** and link them in this README.

This evidence proves your pipeline works end-to-end and makes your submission much stronger!
