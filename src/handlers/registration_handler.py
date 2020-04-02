import json
import requests
import traceback

from src.settings.app import ACCOUNT_TOKEN, DEVICE_CONFIGURATION_URL, DEVICE_NAME, DEVICE_TYPE, DEVICE_TYPE_ATTRIBUTES
from ..settings.registration import *
from .utils import Logger

logs_handler = Logger()
logger = logs_handler.get_logger()


class RegistrationHandler:
    def __init__(self):
        self.registration_status = None

    @staticmethod
    def register():
        # TODO: IMPROVE STATUS CODE PARSING
        try:
            data = dict(thingName=DEVICE_NAME, thingTypeName=DEVICE_TYPE, thingAttributes=dict(attributes=DEVICE_TYPE_ATTRIBUTES))
            headers = {
                "Authorization": f"Bearer {ACCOUNT_TOKEN}",
                "Content-Type": "application/json"
            }
            response = requests.post(url=DEVICE_CONFIGURATION_URL, data=json.dumps(data), headers=headers)
        except Exception:
            logger.error("Something went wrong with registration...")
            logger.error(traceback.format_exc())
            return None
        else:
            # self.registration_status = True
            if response.status_code == 400 and response.json()["failureCode"] == DEVICE_ALREADY_REGISTERED_ERROR:
                logger.error("Device is already registered!")
                return False
            elif response.status_code == 400 and response.json()["failureCode"] == DEVICE_TYPE_DOESNT_EXIST:
                logger.error("Device Type does not exist...")
                return False
            elif response.status_code == 400 and response.json()["failureCode"] == DEVICE_MAXIMUM_REACHED:
                logger.error("Account has reached maximum number of agents")
                return False
            elif response.status_code == 200:
                logger.info(response.json())
                logger.info("Registration was successful!")
                return True
            else:
                logger.error("Uncaptured error...")
                return False

    @staticmethod
    def save_credentials():
        # TODO: SAVE CERTIFICATES IN SPECIFIC DIRECTORY
        pass

