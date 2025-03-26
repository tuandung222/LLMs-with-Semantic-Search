# Terraform Configuration for Semantic Search Deployment

This directory contains Terraform configurations to deploy the semantic search application on Google Kubernetes Engine (GKE).

## Prerequisites

1. Install [Terraform](https://www.terraform.io/downloads.html) (version >= 1.0)
2. Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
3. Configure Google Cloud authentication:
   ```bash
   gcloud auth application-default login
   ```

## Directory Structure

```
terraform/
├── main.tf           # Main Terraform configuration
├── variables.tf      # Variable definitions
├── terraform.tfvars.example  # Example variable values
├── vector-database.md # Vector database deployment guide
└── README.md        # This file
```

## Configuration

1. Copy the example variables file:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```

2. Edit `terraform.tfvars` with your values:
   - `project_id`: Your GCP project ID
   - `region`: GCP region (default: us-central1)
   - `cluster_name`: Name for your GKE cluster
   - `domain`: Domain name for your application
   - `cohere_api_key`: Your Cohere API key
   - Weaviate Configuration (optional):
     - `weaviate_storage_size`: Storage size for Weaviate (default: 10Gi)
     - `weaviate_memory_request`: Memory request (default: 2Gi)
     - `weaviate_memory_limit`: Memory limit (default: 4Gi)
     - `weaviate_cpu_request`: CPU request (default: 500m)
     - `weaviate_cpu_limit`: CPU limit (default: 1000m)

## Deployment

1. Initialize Terraform:
   ```bash
   terraform init
   ```

2. Review the planned changes:
   ```bash
   terraform plan
   ```

3. Apply the configuration:
   ```bash
   terraform apply
   ```

## Infrastructure Components

The configuration creates the following resources:

1. GCP APIs:
   - Container Engine API
   - Artifact Registry API
   - Compute Engine API
   - Cloud Resource Manager API

2. Network:
   - VPC network
   - Subnet
   - Static IP for ingress

3. GKE Cluster:
   - Node pool with e2-medium machines
   - Autoscaling enabled (2-5 nodes)

4. Artifact Registry:
   - Docker repository for container images

5. Vector Database (Weaviate):
   - See [Vector Database Deployment Guide](vector-database.md) for detailed information
   - Persistent storage (10GB by default)
   - Text2Vec Contextionary module enabled
   - Anonymous access enabled
   - Resource limits configured
   - ClusterIP service for internal access

6. Kubernetes Resources:
   - Namespace: semantic-search
   - Secrets: API keys
   - Deployments: API, Demo, and Weaviate
   - Services: API (ClusterIP), Demo (LoadBalancer), and Weaviate (ClusterIP)
   - Ingress: Routes traffic to services
   - Persistent Volumes: Weaviate data storage

## Cleanup

To destroy all created resources:

```bash
terraform destroy
```

## Notes

- The configuration uses the official GKE module from Google
- Node pool autoscaling is enabled to optimize costs
- The API service is internal (ClusterIP) while the demo is external (LoadBalancer)
- Ingress is configured with GCE class for Google Cloud Load Balancing
- Secrets are managed securely using Kubernetes secrets
- Resource limits are set to prevent overconsumption
- Weaviate is configured with persistent storage and optimized for semantic search
- The API service is configured to use Weaviate for vector storage and similarity search

## Additional Documentation

- [Vector Database Deployment Guide](vector-database.md) - Detailed information about deploying and managing the Weaviate vector database

## Troubleshooting

1. If you encounter API enablement issues:
   ```bash
   gcloud services enable container.googleapis.com artifactregistry.googleapis.com compute.googleapis.com cloudresourcemanager.googleapis.com
   ```

2. If you need to check cluster status:
   ```bash
   gcloud container clusters get-credentials $(terraform output -raw cluster_name) --region $(terraform output -raw region)
   kubectl get all -n semantic-search
   ```

3. For ingress issues:
   ```bash
   kubectl describe ingress -n semantic-search
   ```

4. For Weaviate issues, refer to the [Vector Database Deployment Guide](vector-database.md#troubleshooting) 