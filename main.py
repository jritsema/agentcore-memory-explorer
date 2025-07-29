import logging
from log import debug, info, warn, error
from app import app
from config import Config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def main():
    logging.info("Starting agentcore-memory-viewer")
    info({
        "project_name": "agentcore-memory-viewer",
        "status": "starting",
        "config": {
            "region": Config.AWS_REGION,
            "debug": Config.DEBUG,
            "host": Config.HOST,
            "port": Config.PORT
        }
    })
    app.run(
        debug=Config.DEBUG,
        host=Config.HOST,
        port=Config.PORT
    )


if __name__ == "__main__":
    main()
