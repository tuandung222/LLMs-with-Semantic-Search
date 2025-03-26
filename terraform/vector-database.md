# Vector Database Deployment Guide

This guide provides detailed information about deploying and managing the Weaviate vector database for the semantic search application.

## Overview

Weaviate is used as the vector database for storing and retrieving embeddings in the semantic search application. It provides:
- Persistent storage for vector embeddings
- Semantic search capabilities through the Text2Vec Contextionary module
- Scalable architecture for production use
- RESTful API for vector operations

## Deployment Configuration

The vector database is deployed using the following components:

### 1. Weaviate Deployment

```hcl
resource "kubernetes_deployment" "weaviate" {
  metadata {
    name      = "weaviate"
    namespace = "semantic-search"
  }

  spec {
    replicas = 1
    # ... deployment configuration
  }
}
```

Key configuration options:
- `replicas`: Number of Weaviate instances (default: 1)
- `image`: Weaviate container image (default: semitechnologies/weaviate:1.19.6)
- `resources`: CPU and memory limits
- `env`: Environment variables for Weaviate configuration

### 2. Persistent Storage

```hcl
resource "kubernetes_persistent_volume" "weaviate" {
  metadata {
    name = "weaviate-pv"
  }
  spec {
    capacity = {
      storage = var.weaviate_storage_size
    }
    # ... storage configuration
  }
}
```

Storage configuration:
- Storage size: Configurable through `weaviate_storage_size` variable
- Storage class: Uses GCE persistent disk
- Access mode: ReadWriteOnce

### 3. Service Configuration

```hcl
resource "kubernetes_service" "weaviate" {
  metadata {
    name      = "weaviate"
    namespace = "semantic-search"
  }
  spec {
    type = "ClusterIP"
    # ... service configuration
  }
}
```

Service configuration:
- Type: ClusterIP (internal access only)
- Port: 8080
- Target port: 8080

## Environment Variables

The following environment variables configure Weaviate:

| Variable | Description | Default |
|----------|-------------|---------|
| QUERY_DEFAULTS_LIMIT | Maximum number of results per query | 25 |
| AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED | Enable anonymous access | true |
| PERSISTENCE_DATA_PATH | Path for persistent storage | /var/lib/weaviate |
| ENABLE_MODULES | Enabled Weaviate modules | text2vec-contextionary |
| DEFAULT_VECTORIZER_MODULE | Default vectorizer module | text2vec-contextionary |
| CLUSTER_HOSTNAME | Hostname for cluster node | node1 |

## Resource Requirements

Default resource limits and requests:

```hcl
resources {
  requests = {
    memory = var.weaviate_memory_request  # Default: 2Gi
    cpu    = var.weaviate_cpu_request    # Default: 500m
  }
  limits = {
    memory = var.weaviate_memory_limit   # Default: 4Gi
    cpu    = var.weaviate_cpu_limit      # Default: 1000m
  }
}
```

## Configuration Variables

The following variables can be configured in `terraform.tfvars`:

| Variable | Description | Default |
|----------|-------------|---------|
| weaviate_storage_size | Storage size for Weaviate | 10Gi |
| weaviate_memory_request | Memory request | 2Gi |
| weaviate_memory_limit | Memory limit | 4Gi |
| weaviate_cpu_request | CPU request | 500m |
| weaviate_cpu_limit | CPU limit | 1000m |

## Monitoring and Maintenance

### Health Checks

1. Check Weaviate status:
   ```bash
   kubectl exec -n semantic-search deployment/weaviate -- weaviate status
   ```

2. View logs:
   ```bash
   kubectl logs -n semantic-search deployment/weaviate
   ```

3. Check persistent volume:
   ```bash
   kubectl describe pv weaviate-pv
   kubectl describe pvc -n semantic-search weaviate-pvc
   ```

### Backup and Restore

1. Backup Weaviate data:
   ```bash
   kubectl exec -n semantic-search deployment/weaviate -- weaviate backup create backup-name
   ```

2. Restore from backup:
   ```bash
   kubectl exec -n semantic-search deployment/weaviate -- weaviate backup restore backup-name
   ```

## Scaling Considerations

1. **Vertical Scaling**:
   - Adjust CPU and memory limits through Terraform variables
   - Monitor resource usage and adjust as needed

2. **Horizontal Scaling**:
   - Weaviate supports multi-node clusters
   - Update `replicas` in deployment configuration
   - Configure proper cluster settings

3. **Storage Scaling**:
   - Monitor storage usage
   - Consider increasing `weaviate_storage_size` when needed
   - Plan for data growth

## Security Considerations

1. **Access Control**:
   - Weaviate is deployed with anonymous access enabled
   - Consider enabling authentication for production use
   - Use Kubernetes secrets for sensitive data

2. **Network Security**:
   - Weaviate service is internal (ClusterIP)
   - API access is restricted to cluster internal communication
   - Consider implementing network policies

## Troubleshooting

Common issues and solutions:

1. **Storage Issues**:
   ```bash
   # Check storage status
   kubectl describe pv weaviate-pv
   kubectl describe pvc -n semantic-search weaviate-pvc
   
   # Check storage usage
   kubectl exec -n semantic-search deployment/weaviate -- df -h /var/lib/weaviate
   ```

2. **Performance Issues**:
   ```bash
   # Check resource usage
   kubectl top pod -n semantic-search -l app=weaviate
   
   # Check logs for errors
   kubectl logs -n semantic-search deployment/weaviate
   ```

3. **Connection Issues**:
   ```bash
   # Test Weaviate connectivity
   kubectl exec -n semantic-search deployment/weaviate -- curl localhost:8080/v1/meta
   ```

## Best Practices

1. **Resource Management**:
   - Monitor resource usage regularly
   - Set appropriate limits and requests
   - Plan for growth

2. **Backup Strategy**:
   - Regular backups of vector data
   - Test restore procedures
   - Document backup/restore procedures

3. **Security**:
   - Regular security updates
   - Access control implementation
   - Network security policies

4. **Monitoring**:
   - Implement monitoring solutions
   - Set up alerts for critical issues
   - Regular health checks 