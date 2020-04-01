import schedule
import time

from .handlers.utils import Logger
from .settings.app import DEVICE_SYNC_TIME

logs_handler = Logger()
logger = logs_handler.get_logger()


def test_job():
    logger.info(f"Job at {time.time()}")


if __name__ == "__main__":
    logger.info("Starting application!")

    # Example function
    schedule.every(int(DEVICE_SYNC_TIME)).seconds.do(test_job)

    # TODO: Add Registration handler
    # TODO: Add MQTT Connection, Publish and Subscription handler
    # TODO: Add other scheduled functions to collect hardware and send them to the cloud using MQTT

    while True:
        schedule.run_pending()
        time.sleep(1)
