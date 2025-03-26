# GitHub Actions CI/CD Workflow

This directory contains the GitHub Actions workflow configurations for the Semantic Search project's continuous integration and continuous deployment (CI/CD) pipeline.

## Workflow Files

- **docker-build-push.yml**: Builds and pushes Docker images to Docker Hub, then runs integration tests

## Workflow Details

### Build and Push Process

1. The workflow checks out the code repository
2. Sets up Docker Buildx for multi-platform builds
3. Logs in to Docker Hub using credentials stored as GitHub secrets
4. Extracts metadata for container images (tags, labels)
5. Builds and pushes the following images:
   - Search Server: `tuandung12092002/semantic-search-server`
   - Demo App: `tuandung12092002/semantic-search-demo`

### Testing Process

After building and pushing the images, the workflow:

1. Deploys the application using Docker Compose
2. Waits for all services to become healthy
3. Runs integration tests against the deployed services
4. Cleans up resources after tests complete

## Required GitHub Secrets

To use this workflow, configure the following secrets in your GitHub repository:

- `DOCKERHUB_TOKEN`: A Docker Hub access token with push permissions
- `OPENAI_API_KEY`: Your OpenAI API key for testing

## Local Workflow Testing

You can test the workflow locally before pushing to GitHub using [act](https://github.com/nektos/act):

```bash
# Install act
brew install act  # macOS
# or follow installation instructions for your platform

# Run the workflow locally
act -s DOCKERHUB_TOKEN=your_token -s OPENAI_API_KEY=your_key
```

## Customizing the Workflow

### Adding More Tests

To add additional tests, modify the "Test Search API" step in the workflow file:

```yaml
- name: Test Search API
  run: |
    # Add your custom test commands here
    # Be sure to check for expected results and exit with non-zero status on failure
```

### Building for Multiple Platforms

To build images for multiple platforms (e.g., arm64, amd64), modify the build step:

```yaml
- name: Build and Push Search Server Image
  uses: docker/build-push-action@v4
  with:
    # Add these lines:
    platforms: linux/amd64,linux/arm64
    # Rest of config...
```

## Troubleshooting

### Common Issues

1. **Authentication Failures**: Ensure your Docker Hub token has not expired and has the correct permissions

2. **Slow Builds**: Consider using GitHub-hosted caching to speed up builds:
   ```yaml
   - name: Cache Docker layers
     uses: actions/cache@v3
     with:
       path: /tmp/.buildx-cache
       key: ${{ runner.os }}-buildx-${{ github.sha }}
       restore-keys: |
         ${{ runner.os }}-buildx-
   ```

3. **Failed Tests**: Check logs for specific errors and adjust timeouts if services need more time to start 