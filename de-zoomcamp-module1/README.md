# Data Engineering Zoomcamp - Module 1: Containerization and Infrastructure as Code

This repository contains the homework and practice materials for Module 1 of the Data Engineering Zoomcamp. The focus of this module is on Docker, PostgreSQL, and Terraform.

## 📁 Project Structure

```text
de-zoomcamp-module1/
├── terraform/                # Terraform configuration for GCP
│   ├── main.tf               # GCS and BigQuery resource definitions
│   ├── variables.tf          # Variable declarations
│   ├── terraform.tfvars      # Variable values (Project ID, etc.)
│   └── README.md             # Terraform setup instructions
├── docker-compose.yaml       # Docker services (Postgres, pgAdmin)
├── load_data.py              # Python script for data ingestion
├── check_answers.py          # Script to verify homework SQL results
├── init_schema.sql           # Initial SQL schema (optional)
├── green_tripdata_2025-11.parquet # Dataset: Green Taxi trips
└── taxi_zone_lookup.csv      # Dataset: Taxi zones
```

## 🛠️ Prerequisites

- **Docker & Docker Compose**: To run PostgreSQL and pgAdmin.
- **Python 3.10+**: To run the ingestion scripts.
- **Terraform**: To provision GCP infrastructure.
- **GCP Account**: A Google Cloud Project for Terraform practice.

## 🚀 Getting Started

### 1. Docker Environment

Start the PostgreSQL and pgAdmin containers:

```bash
docker-compose up -d
```

*Note: Postgres will be available on `localhost:5433` (mapped from 5432).*

### 2. Data Ingestion

Load the NYC Taxi data into the PostgreSQL database:

```bash
# Set the port to 5433 for external access
$env:POSTGRES_PORT="5433"
python load_data.py
```

This will:
- Load **46,912** rows into the `green_tripdata` table.
- Load **265** rows into the `taxi_zone_lookup` table.

### 3. Terraform (GCP)

Navigate to the terraform directory to manage your cloud resources:

```bash
cd terraform
# Follow instructions in terraform/README.md
```

## 📊 SQL Homework Queries

You can verify the homework answers by running the provided script:

```bash
python check_answers.py
```

### Key Queries Covered:
- **Q3**: Counting trips with distance ≤ 1 mile in Nov 2025.
- **Q4**: Finding the day with the longest trip distance.
- **Q5**: Finding the pickup zone with the largest total amount on Nov 18, 2025.
- **Q6**: Finding the drop-off zone with the largest tip for "East Harlem North" pickups.

## 📝 Important Notes

- **Database Credentials**: Default user/password is `postgres/postgres`.
- **Database Name**: `ny_taxi`.
- **Terraform**: Ensure you update `terraform.tfvars` with your specific `project_id`.

---
*Created for the Data Engineering Zoomcamp - 2026*
