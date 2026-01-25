# Terraform GCP Infrastructure Setup

This directory contains Terraform configuration for setting up GCP resources for the DE Zoomcamp Module 1.

## Resources Created

- **GCS Bucket**: For storing data files
- **BigQuery Dataset**: For data warehouse operations

## Prerequisites

1. **Install Terraform**: Download from [terraform.io](https://www.terraform.io/downloads)
2. **GCP Account**: Active Google Cloud Platform account
3. **Service Account**: Create a service account with the following roles:
   - Storage Admin
   - BigQuery Admin
4. **Service Account Key**: Download JSON key file

## Setup Instructions

### 1️⃣ Configure GCP Credentials

```bash
# Set the path to your service account key
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
```

### 2️⃣ Update Configuration

Edit `terraform.tfvars` and replace `your-gcp-project-id` with your actual GCP project ID:

```hcl
project_id    = "your-actual-gcp-project-id"  # ⚠️ UPDATE THIS
bucket_name   = "de-zoomcamp-bucket-2026"
dataset_name  = "de_zoomcamp_dataset"
region        = "us-central1"
```

> **Note**: The bucket name must be globally unique. If the name is taken, modify `bucket_name` to something unique.

### 3️⃣ Initialize Terraform

```bash
cd terraform
terraform init
```

This will download the Google Cloud provider plugin.

### 4️⃣ Review the Plan

```bash
terraform plan
```

This shows what resources will be created.

### 5️⃣ Apply Configuration

```bash
# With confirmation prompt
terraform apply

# Or auto-approve (skip confirmation)
terraform apply -auto-approve
```

### 6️⃣ Verify Resources

After successful apply, you can verify:

```bash
# List GCS buckets
gcloud storage buckets list

# List BigQuery datasets
bq ls
```

## Cleanup

To destroy all resources created by Terraform:

```bash
terraform destroy -auto-approve
```

## Outputs

After applying, you'll see:
- ✅ GCS bucket created at: `gs://de-zoomcamp-bucket-2026`
- ✅ BigQuery dataset created: `de_zoomcamp_dataset`

## Troubleshooting

### Authentication Error
```
Error: google: could not find default credentials
```
**Solution**: Set `GOOGLE_APPLICATION_CREDENTIALS` environment variable

### Bucket Already Exists
```
Error: Error creating bucket: googleapi: Error 409: conflict
```
**Solution**: Change `bucket_name` in `terraform.tfvars` to a unique name

### Permission Denied
```
Error: Error creating dataset: Access Denied
```
**Solution**: Ensure your service account has the required permissions

## File Structure

```
terraform/
├── main.tf              # Main configuration with resources
├── variables.tf         # Variable definitions
├── terraform.tfvars     # Variable values (update this!)
└── README.md           # This file
```

## Important Notes

⚠️ **Before running terraform apply**:
1. Update `terraform.tfvars` with your actual GCP project ID
2. Set `GOOGLE_APPLICATION_CREDENTIALS` environment variable
3. Ensure your service account has the necessary permissions
4. Verify the bucket name is globally unique

---

**DataTalks.Club DE Zoomcamp - Module 1**
