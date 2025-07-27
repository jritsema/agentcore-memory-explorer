# Technology Stack

## Runtime & Language

- **Python**: 3.13.1 (specified in .tool-versions)
- **Virtual Environment**: Uses `.venv` with direnv for automatic activation

## Dependencies

- **boto3**: AWS SDK for Python - primary dependency for Bedrock AgentCore Memory API integration
- **Standard Library**: logging, json for application logging and data handling

## Build System & Tools

- **Make**: Primary build automation tool
- **pip**: Package management with requirements.txt and piplock.txt
- **direnv**: Environment management (auto-activates .venv)
- **Docker**: Containerization support with Python 3.11-slim base image

## Common Commands

### Development Setup

```bash
make init          # Initialize Python virtual environment
make install       # Install all dependencies from piplock.txt
make install <pkg> # Add new package to requirements.txt and install
```

### Running the Application

```bash
make start         # Run the application locally
```

### Docker

```bash
docker build -t agentcore-memory-viewer .
docker run agentcore-memory-viewer
```

## Development Workflow

1. Use `make init` for initial setup
2. Add dependencies with `make install <package>` (automatically updates requirements.txt and piplock.txt)
3. Use `make start` for local development
4. Dependencies are locked in piplock.txt for reproducible builds
