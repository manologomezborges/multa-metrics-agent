import json
import requests
import traceback

from src.settings.app import ACCOUNT_TOKEN, DEVICE_CONFIGURATION_URL, DEVICE_NAME, DEVICE_TYPE, DEVICE_TYPE_ATTRIBUTES
from src.settings.registration import *
from src.settings.mqtt import DEVICE_PEM_FILE, DEVICE_PRIVATE_KEY_FILE, DEVICE_PUBLIC_KEY_FILE, ROOTCA_CERTIFICATE_FILE
from src.handlers.utils import Logger

logs_handler = Logger()
logger = logs_handler.get_logger()


class RegistrationHandler:
    def __init__(self):
        pass

    @staticmethod
    def register():
        data = dict(
            thingName=DEVICE_NAME, thingTypeName=DEVICE_TYPE, thingAttributes=dict(attributes=DEVICE_TYPE_ATTRIBUTES)
        )
        headers = {"Authorization": f"Bearer {ACCOUNT_TOKEN}", "Content-Type": "application/json"}
        try:
            response = requests.post(url=DEVICE_CONFIGURATION_URL, data=json.dumps(data), headers=headers)
            response.raise_for_status()
        except requests.HTTPError:
            logger.error("Something went wrong with registration...")
            logger.error(traceback.format_exc())
            if response.status_code == 400 and response.json()["failureCode"] == DEVICE_ALREADY_REGISTERED_ERROR:
                logger.error("Device is already registered!")
                return False
            elif response.status_code == 400 and response.json()["failureCode"] == DEVICE_TYPE_DOESNT_EXIST:
                logger.error("Device Type does not exist...")
                return False
            elif response.status_code == 400 and response.json()["failureCode"] == DEVICE_MAXIMUM_REACHED:
                logger.error("Account has reached maximum number of agents")
                return False
            else:
                return None
        except Exception:
            logger.error("Uncaptured error...")
            logger.error(traceback.format_exc())
            return None
        else:
            logger.info("Registration was successful!")
            return response.json()

    @staticmethod
    def save_credentials(credentials_dictionary, root_ca):
        try:
            logger.info("Saving certificate files...")
            with open(DEVICE_PEM_FILE, "w") as pem_certificate_file:
                pem_certificate_file.write(credentials_dictionary["pem"])
            with open(DEVICE_PRIVATE_KEY_FILE, "w") as private_key_file:
                private_key_file.write(credentials_dictionary["key_pair"]["private_key"])
            with open(DEVICE_PUBLIC_KEY_FILE, "w") as public_key_file:
                public_key_file.write(credentials_dictionary["key_pair"]["public_key"])
            with open(ROOTCA_CERTIFICATE_FILE, "w") as root_ca_file:
                root_ca_file.write(root_ca)
        except Exception:
            logger.error("Error saving certificate files...")
            logger.error(traceback.format_exc())
            return False
        else:
            logger.info("Certificates saved correctly")
            return True

    @staticmethod
    def clean_credentials():
        pass
