terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# ==========================
# Create a GCS Bucket
# ==========================
resource "google_storage_bucket" "de_zoomcamp_bucket" {
  name          = var.bucket_name
  location      = var.region
  force_destroy = true
}

# ==========================
# Create a BigQuery Dataset
# ==========================
resource "google_bigquery_dataset" "de_zoomcamp_dataset" {
  dataset_id = var.dataset_name
  location   = var.region
}
