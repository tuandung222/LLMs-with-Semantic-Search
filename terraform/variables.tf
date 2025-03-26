variable "project_id" {
  description = "The project ID to deploy to"
  type        = string
}

variable "region" {
  description = "The region to deploy to"
  type        = string
  default     = "us-central1"
}

variable "gke_num_nodes" {
  description = "Number of GKE nodes"
  type        = number
  default     = 2
}

variable "cluster_name" {
  description = "The name of the GKE cluster"
  type        = string
  default     = "semantic-search-cluster"
}

variable "domain" {
  description = "The domain name for the application"
  type        = string
}

variable "openai_api_key" {
  description = "The OpenAI API key"
  type        = string
  sensitive   = true
}

variable "weaviate_storage_size" {
  description = "Storage size for Weaviate persistent volume"
  type        = string
  default     = "10Gi"
}

variable "weaviate_memory_request" {
  description = "Memory request for Weaviate container"
  type        = string
  default     = "2Gi"
}

variable "weaviate_memory_limit" {
  description = "Memory limit for Weaviate container"
  type        = string
  default     = "4Gi"
}

variable "weaviate_cpu_request" {
  description = "CPU request for Weaviate container"
  type        = string
  default     = "500m"
}

variable "weaviate_cpu_limit" {
  description = "CPU limit for Weaviate container"
  type        = string
  default     = "1000m"
}

variable "weaviate_api_key" {
  description = "The Weaviate API key"
  type        = string
  sensitive   = true
} 