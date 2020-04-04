import schedule
import sys
import time

from src.handlers.registration_handler import RegistrationHandler, register_device
from src.handlers.utils import Logger
from src.settings.app import DEVICE_SYNC_TIME

logs_handler = Logger()
logger = logs_handler.get_logger()


def test_job():
    logger.info(f"Job at {time.time()}")


if __name__ == "__main__":
    logger.info("Starting application!")

    # Example function
    schedule.every(int(DEVICE_SYNC_TIME)).seconds.do(test_job)
    try:
        if RegistrationHandler.check_credentials() is False:
            logger.info("Unable to find device credentials, starting registration...")
            register_device()
        else:
            logger.info("Agent is already registered")

    except RuntimeError:
        logger.error("Error registering and saving credentials...")
        sys.exit(1)

    # TODO: Add MQTT Connection, Publish and Subscription handler
    # TODO: Add other scheduled functions to collect hardware and send them to the cloud using MQTT

    while True:
        schedule.run_pending()
        time.sleep(1)
