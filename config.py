import os


class Config:
    """Application configuration"""

    # AWS Configuration
    AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
    AWS_PROFILE = os.environ.get('AWS_PROFILE', None)

    # Flask Configuration
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
    PORT = int(os.environ.get('FLASK_PORT', 5000))

    # Pagination defaults
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100

    # UI Configuration
    APP_TITLE = "AgentCore Memory Viewer"
    AUTO_REFRESH_INTERVAL = 30  # seconds
