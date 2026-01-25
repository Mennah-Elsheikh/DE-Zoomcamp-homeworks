variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "bucket_name" {
  description = "GCS bucket name"
  type        = string
}

variable "dataset_name" {
  description = "BigQuery dataset name"
  type        = string
}
