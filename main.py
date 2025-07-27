import logging
from log import debug, info, warn, error

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def main():
    logging.info("agentcore-memory-viewer")
    info({"project_name": "agentcore-memory-viewer"})


if __name__ == "__main__":
    main()
