import os

DEVICE_CONFIGURATION_URL = os.environ.get("DEVICE_CONFIGURATION_URL", "https://cvm-agent.dev.multa.io/multa-agent/")

DEVICE_ALREADY_REGISTERED_ERROR = os.environ.get("DEVICE_ALREADY_REGISTERED_ERROR", 1)
DEVICE_TYPE_DOESNT_EXIST = os.environ.get("DEVICE_TYPE_DOESNT_EXIST", 2)
DEVICE_MAXIMUM_REACHED = os.environ.get("DEVICE_MAXIMUM_REACHED", 3)
