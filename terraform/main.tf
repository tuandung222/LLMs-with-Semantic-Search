terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 4.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}

# Enable required APIs
resource "google_project_service" "required_apis" {
  for_each = toset([
    "container.googleapis.com",
    "artifactregistry.googleapis.com",
    "compute.googleapis.com",
    "cloudresourcemanager.googleapis.com"
  ])

  project = var.project_id
  service = each.key

  disable_on_destroy = false
}

# Create GKE cluster
resource "google_container_cluster" "primary" {
  name     = "${var.project_id}-gke"
  location = var.region

  # We can't create a cluster with no node pool defined, but we want to only use
  # separately managed node pools. So we create the smallest possible default
  # node pool and immediately delete it.
  remove_default_node_pool = true
  initial_node_count       = 1
}

# Create node pool
resource "google_container_node_pool" "primary_nodes" {
  name       = "${google_container_cluster.primary.name}-node-pool"
  location   = var.region
  cluster    = google_container_cluster.primary.name
  node_count = var.gke_num_nodes

  node_config {
    oauth_scopes = [
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
    ]

    labels = {
      env = var.project_id
    }

    machine_type = "e2-standard-4"
    disk_size_gb = 50
    disk_type    = "pd-standard"
  }
}

# Create VPC network
resource "google_compute_network" "vpc" {
  name                    = "${var.project_id}-vpc"
  auto_create_subnetworks = false
}

# Create subnet
resource "google_compute_subnetwork" "subnet" {
  name          = "${var.project_id}-subnet"
  region        = var.region
  network       = google_compute_network.vpc.name
  ip_cidr_range = "10.0.0.0/24"
}

# Create Artifact Registry repository
resource "google_artifact_registry_repository" "repo" {
  location      = var.region
  repository_id = "semantic-search"
  description   = "Docker repository for semantic search application"
  format        = "DOCKER"
}

# Create static IP for ingress
resource "google_compute_global_address" "ingress_ip" {
  name = "semantic-search-ip"
}

# Configure Kubernetes provider
provider "kubernetes" {
  host                   = "https://${google_container_cluster.primary.endpoint}"
  token                  = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(google_container_cluster.primary.master_auth[0].cluster_ca_certificate)
}

data "google_client_config" "default" {}

# Create namespace
resource "kubernetes_namespace" "semantic_search" {
  metadata {
    name = "semantic-search"
  }
}

# Create storage class for Weaviate
resource "kubernetes_storage_class" "weaviate_storage" {
  metadata {
    name = "weaviate-storage"
  }
  storage_provisioner = "kubernetes.io/gce-pd"
  reclaim_policy     = "Retain"
  parameters = {
    type = "pd-standard"
  }
}

# Output the cluster endpoint and credentials
output "cluster_endpoint" {
  value = google_container_cluster.primary.endpoint
}

output "cluster_ca_certificate" {
  value = google_container_cluster.primary.master_auth[0].cluster_ca_certificate
}

output "cluster_name" {
  value = google_container_cluster.primary.name
}

# Create Kubernetes secret for API keys
resource "kubernetes_secret" "api_secrets" {
  metadata {
    name      = "api-secrets"
    namespace = kubernetes_namespace.semantic_search.metadata[0].name
  }

  data = {
    "openai-api-key" = var.openai_api_key
    "weaviate-api-key" = var.weaviate_api_key
  }
}

# Deploy API application
resource "kubernetes_deployment" "api" {
  metadata {
    name      = "semantic-search-api"
    namespace = kubernetes_namespace.semantic_search.metadata[0].name
  }

  spec {
    replicas = 2

    selector {
      match_labels = {
        app = "semantic-search-api"
      }
    }

    template {
      metadata {
        labels = {
          app = "semantic-search-api"
        }
      }

      spec {
        container {
          name  = "api"
          image = "${var.region}-docker.pkg.dev/${var.project_id}/semantic-search/semantic-search-api:latest"

          port {
            container_port = 8000
          }

          env {
            name = "OPENAI_API_KEY"
            value_from {
              secret_key_ref {
                name = kubernetes_secret.api_secrets.metadata[0].name
                key  = "openai-api-key"
              }
            }
          }

          env {
            name  = "WEAVIATE_URL"
            value = "http://weaviate:8080"
          }

          env {
            name  = "WEAVIATE_API_KEY"
            value_from {
              secret_key_ref {
                name = kubernetes_secret.api_secrets.metadata[0].name
                key  = "weaviate-api-key"
              }
            }
          }

          resources {
            requests = {
              memory = "512Mi"
              cpu    = "250m"
            }
            limits = {
              memory = "1Gi"
              cpu    = "500m"
            }
          }
        }
      }
    }
  }
}

# Create API service
resource "kubernetes_service" "api" {
  metadata {
    name      = "semantic-search-api"
    namespace = kubernetes_namespace.semantic_search.metadata[0].name
  }

  spec {
    selector = {
      app = "semantic-search-api"
    }

    port {
      port        = 80
      target_port = 8000
    }

    type = "ClusterIP"
  }
}

# Deploy Demo application
resource "kubernetes_deployment" "demo" {
  metadata {
    name      = "semantic-search-demo"
    namespace = kubernetes_namespace.semantic_search.metadata[0].name
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "semantic-search-demo"
      }
    }

    template {
      metadata {
        labels = {
          app = "semantic-search-demo"
        }
      }

      spec {
        container {
          name  = "demo"
          image = "${var.region}-docker.pkg.dev/${var.project_id}/semantic-search/semantic-search-demo:latest"

          port {
            container_port = 8501
          }

          env {
            name  = "API_URL"
            value = "http://semantic-search-api"
          }

          env {
            name  = "OPENAI_API_KEY"
            value_from {
              secret_key_ref {
                name = kubernetes_secret.api_secrets.metadata[0].name
                key  = "openai-api-key"
              }
            }
          }

          env {
            name  = "WEAVIATE_API_KEY"
            value_from {
              secret_key_ref {
                name = kubernetes_secret.api_secrets.metadata[0].name
                key  = "weaviate-api-key"
              }
            }
          }

          resources {
            requests = {
              memory = "256Mi"
              cpu    = "100m"
            }
            limits = {
              memory = "512Mi"
              cpu    = "200m"
            }
          }
        }
      }
    }
  }
}

# Create Demo service
resource "kubernetes_service" "demo" {
  metadata {
    name      = "semantic-search-demo"
    namespace = kubernetes_namespace.semantic_search.metadata[0].name
  }

  spec {
    selector = {
      app = "semantic-search-demo"
    }

    port {
      port        = 80
      target_port = 8501
    }

    type = "LoadBalancer"
  }
}

# Create Ingress
resource "kubernetes_ingress_v1" "ingress" {
  metadata {
    name      = "semantic-search-ingress"
    namespace = kubernetes_namespace.semantic_search.metadata[0].name
    annotations = {
      "kubernetes.io/ingress.class"           = "gce"
      "kubernetes.io/ingress.global-static-ip-name" = google_compute_global_address.ingress_ip.name
    }
  }

  spec {
    rule {
      host = "api.${var.domain}"
      http {
        path {
          path      = "/"
          path_type = "Prefix"
          backend {
            service {
              name = kubernetes_service.api.metadata[0].name
              port {
                number = 80
              }
            }
          }
        }
      }
    }

    rule {
      host = "demo.${var.domain}"
      http {
        path {
          path      = "/"
          path_type = "Prefix"
          backend {
            service {
              name = kubernetes_service.demo.metadata[0].name
              port {
                number = 80
              }
            }
          }
        }
      }
    }
  }
}

# Create Weaviate deployment
resource "kubernetes_deployment" "weaviate" {
  metadata {
    name      = "weaviate"
    namespace = kubernetes_namespace.semantic_search.metadata[0].name
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "weaviate"
      }
    }

    template {
      metadata {
        labels = {
          app = "weaviate"
        }
      }

      spec {
        container {
          name  = "weaviate"
          image = "semitechnologies/weaviate:1.19.6"

          port {
            container_port = 8080
          }

          env {
            name  = "QUERY_DEFAULTS_LIMIT"
            value = "25"
          }

          env {
            name  = "AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED"
            value = "true"
          }

          env {
            name  = "PERSISTENCE_DATA_PATH"
            value = "/var/lib/weaviate"
          }

          env {
            name  = "ENABLE_MODULES"
            value = "text2vec-contextionary"
          }

          env {
            name  = "DEFAULT_VECTORIZER_MODULE"
            value = "text2vec-contextionary"
          }

          env {
            name  = "CLUSTER_HOSTNAME"
            value = "node1"
          }

          env {
            name  = "WEAVIATE_API_KEY"
            value_from {
              secret_key_ref {
                name = kubernetes_secret.api_secrets.metadata[0].name
                key  = "weaviate-api-key"
              }
            }
          }

          resources {
            requests = {
              memory = "2Gi"
              cpu    = "500m"
            }
            limits = {
              memory = "4Gi"
              cpu    = "1000m"
            }
          }

          volume_mount {
            name       = "weaviate-data"
            mount_path = "/var/lib/weaviate"
          }
        }

        volume {
          name = "weaviate-data"
          persistent_volume_claim {
            claim_name = kubernetes_persistent_volume_claim.weaviate.metadata[0].name
          }
        }
      }
    }
  }
}

# Create Weaviate service
resource "kubernetes_service" "weaviate" {
  metadata {
    name      = "weaviate"
    namespace = kubernetes_namespace.semantic_search.metadata[0].name
  }

  spec {
    selector = {
      app = "weaviate"
    }

    port {
      port        = 8080
      target_port = 8080
    }

    type = "ClusterIP"
  }
}

# Create persistent volume for Weaviate
resource "kubernetes_persistent_volume" "weaviate" {
  metadata {
    name = "weaviate-pv"
  }

  spec {
    capacity = {
      storage = "10Gi"
    }

    access_modes = ["ReadWriteOnce"]

    storage_class_name = "standard"

    persistent_volume_source {
      gce_persistent_disk {
        pd_name = "weaviate-data"
        fs_type = "ext4"
      }
    }
  }
}

# Create persistent volume claim for Weaviate
resource "kubernetes_persistent_volume_claim" "weaviate" {
  metadata {
    name      = "weaviate-pvc"
    namespace = kubernetes_namespace.semantic_search.metadata[0].name
  }

  spec {
    access_modes = ["ReadWriteOnce"]

    resources {
      requests = {
        storage = "10Gi"
      }
    }

    storage_class_name = "standard"
  }
}

resource "aws_secretsmanager_secret" "api_keys" {
  name = "${var.cluster_name}-api-keys"
}

resource "aws_secretsmanager_secret_version" "api_keys" {
  secret_id = aws_secretsmanager_secret.api_keys.id
  secret_string = jsonencode({
    "openai-api-key" = var.openai_api_key
    "weaviate-api-key" = var.weaviate_api_key
  })
}

resource "aws_ssm_parameter" "openai_api_key" {
  name  = "/${var.cluster_name}/openai-api-key"
  type  = "SecureString"
  value = var.openai_api_key
} 