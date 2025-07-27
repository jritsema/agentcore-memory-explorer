# Project Structure

## Root Directory Layout

```
agentcore-memory-viewer/
├── main.py              # Application entry point
├── log.py               # Custom JSON logging utilities
├── requirements.txt     # Direct dependencies
├── piplock.txt          # Locked dependency versions
├── Makefile            # Build automation and common tasks
├── Dockerfile          # Container configuration
├── README.md           # Project documentation
├── .envrc              # direnv configuration for .venv activation
├── .tool-versions      # asdf/mise tool version specifications
├── .dockerignore       # Docker build exclusions
├── .gitignore          # Git exclusions
├── .venv/              # Python virtual environment
└── .kiro/              # Kiro AI assistant configuration
    └── steering/       # AI guidance documents
```

## Code Organization

### Core Application Files

- **main.py**: Entry point with basic logging setup and main() function
- **log.py**: Centralized logging utilities with JSON output formatting

### Configuration Files

- **requirements.txt**: High-level dependencies (currently just boto3)
- **piplock.txt**: Exact dependency versions for reproducible builds
- **.envrc**: Automatically activates Python virtual environment via direnv

## Conventions

### Python Code Style

- Use standard Python logging module with INFO level by default
- JSON-formatted output for structured logging via custom log.py utilities
- Import custom logging functions: `from log import debug, info, warn, error`

### Dependency Management

- Add new packages via `make install <package>` (updates both requirements.txt and piplock.txt)
- Keep requirements.txt minimal with direct dependencies only
- Use piplock.txt for exact version pinning

### File Naming

- Snake_case for Python modules
- Lowercase with hyphens for project name and Docker image
- Standard Python conventions for imports and module structure
