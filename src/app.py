import schedule
import time

from src.handlers.registration_handler import RegistrationHandler
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

    # TODO: Add Registration handler
    registration_status = RegistrationHandler.register()
    while registration_status is None:
        logger.error("Error registering device... Trying again in 1 minute...")
        time.sleep(60)
        registration_status = RegistrationHandler.register()

    logger.info(f"Registration was: {registration_status}")

    # TODO: Add MQTT Connection, Publish and Subscription handler
    # TODO: Add other scheduled functions to collect hardware and send them to the cloud using MQTT

    while True:
        schedule.run_pending()
        time.sleep(1)
