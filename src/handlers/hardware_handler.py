from datetime import datetime
import time
import traceback

import psutil
from psutil._common import bytes2human

from .utils import Logger


logs_handler = Logger()
logger = logs_handler.get_logger()


class HWAnalyzer:
    def __init__(self):
        try:
            self.ram_info = psutil.virtual_memory()
            self.os_disk_info = psutil.disk_usage(path="/")
            self.cpu_info = psutil.cpu_percent(interval=0.1)
            self.temperature = psutil.sensors_temperatures(fahrenheit=True)["coretemp"]
            self.boot_time = psutil.boot_time()

        except Exception:
            logger.error("Error getting necessary system information")
            logger.error(traceback.format_exc())
            self.ram_info = None
            self.os_disk_info = None
            self.cpu_info = None
            self.temperature = None

    def get_current_ram(self):
        """Gets current RAM usage and returns it in human verbosity"""
        try:
            return bytes2human(self.ram_info.total - self.ram_info.available)
        except Exception:
            logger.error(traceback.format_exc())
            raise RuntimeError

    def get_total_ram(self):
        """Gets total RAM capacity and returns it in human verbosity"""
        try:
            return bytes2human(self.ram_info.total)
        except Exception:
            logger.error(traceback.format_exc())
            raise RuntimeError

    def get_percentage_and_threshold_ram(self):
        """Gets usage percent and evaluates if it's high based on threshold"""
        try:
            percent = self.ram_info.percent
            if percent >= 80:
                high = True
            else:
                high = False

            return percent, high

        except Exception:
            logger.error(traceback.format_exc())
            raise RuntimeError

    def get_current_disk(self):
        """Gets current disk usage and returns it in human verbosity"""
        try:
            return bytes2human(self.os_disk_info.used)
        except Exception:
            logger.error(traceback.format_exc())
            raise RuntimeError

    def get_total_disk(self):
        """Gets total disk capacity and returns it in human verbosity"""
        try:
            return bytes2human(self.os_disk_info.total)
        except Exception:
            logger.error(traceback.format_exc())
            raise RuntimeError

    def get_percentage_and_threshold_disk(self):
        """Gets usage percent and evaluates if it's high based on threshold"""
        try:
            os_percent = self.os_disk_info.percent
            if os_percent >= 80:
                os_high = True
            else:
                os_high = False

            return os_percent, os_high

        except Exception:
            logger.error(traceback.format_exc())
            raise RuntimeError

    @staticmethod
    def get_percentage_and_threshold_cpu():
        """
        Gets usage percent and evaluates if it's high based on threshold. In CPU case is better to
        have a set of measurements and get the mean value of them.
        """
        try:
            measurements = 10
            usage = []
            for element in list(range(1, measurements + 1)):
                time.sleep(0.25)
                usage.append(psutil.cpu_percent(interval=0.1))

            cpu_usage_average_percent = sum(usage) / len(usage)
            if cpu_usage_average_percent >= 80:
                high = True
            else:
                high = False

            return round(cpu_usage_average_percent, 1), high

        except Exception:
            logger.error(traceback.format_exc())
            raise RuntimeError

    def get_current_temperature_average(self):
        """
        Gets the current temperature usage in Fahrenheit degrees. In order to get a customer-facing
        reading, we average the temperature in all the cores.
        """
        try:
            usage = []
            for core in self.temperature:
                usage.append(core.current)

            temperature_usage_average = sum(usage) / len(usage)
            return round(temperature_usage_average, 1)

        except Exception:
            logger.error(traceback.format_exc())
            raise RuntimeError

    def get_max_temperature_average(self):
        """
        Gets the max temperature usage in Fahrenheit degrees. In order to get a customer-facing
        reading, we average the temperature in all the cores.
        """
        try:
            all_equal = all(core.high == self.temperature[0].high for core in self.temperature)
            if all_equal is True:
                return self.temperature[0].high

            else:
                max_temps = []
                for core in self.temperature:
                    max_temps.append(core.high)
                high_temperature_average = sum(max_temps) / len(max_temps)
                return high_temperature_average

        except Exception:
            logger.error(traceback.format_exc())
            raise RuntimeError

    def get_percentage_and_threshold_temperature(self):
        """
        Gets usage percent and evaluates if it's high based on threshold. In temperature case is
        better to have it based in averages value than per-core value.
        """
        try:
            current_temp_average = self.get_current_temperature_average()
            high_temp_average = self.get_max_temperature_average()

            percent = (current_temp_average / high_temp_average) * 100
            if percent >= 80:
                high = True
            else:
                high = False

            return round(percent, 1), high
        except Exception:
            logger.error(traceback.format_exc())
            raise RuntimeError

    def get_device_uptime(self):
        """
        Gets the device uptime (date), gets the time since the device uptime and sets a threshold
        for to evaluate if the device has been on for too much time.
        :return:
        """
        try:
            boot_date = datetime.fromtimestamp(self.boot_time)
            current_date = datetime.now()

            days_since_boot = (current_date - boot_date).days
            seconds_since_boot = round(time.time() - psutil.boot_time())

            threshold = 7
            if days_since_boot > threshold:
                threshold_crossed = True
            else:
                threshold_crossed = False

            return boot_date, seconds_since_boot, threshold_crossed

        except Exception:
            logger.error(traceback.format_exc())
            raise RuntimeError

    @staticmethod
    def get_interface_data(interface: str):
        """
        Return always bytes amount because is used for data storage client in Influx.
        :param interface:
        :return: int
        """
        try:
            return (
                psutil.net_io_counters(pernic=True)[interface].bytes_sent
                + psutil.net_io_counters(pernic=True)[interface].bytes_recv
            )
        except Exception:
            raise RuntimeError

    @staticmethod
    def get_lte_interface_name():
        try:
            for element in psutil.net_io_counters(pernic=True):
                if "wwp0" in element:
                    return element
        except Exception:
            logger.error(traceback.format_exc())
            raise RuntimeError

    @staticmethod
    def bytes_int_2_human(meausure: int):
        try:
            return bytes2human(meausure)
        except Exception:
            raise RuntimeError

    @staticmethod
    def bytes_dict_2_human(data_dictionary: dict):
        try:
            for key, value in data_dictionary.items():
                data_dictionary[key] = bytes2human(value)
            return data_dictionary
        except Exception:
            logger.error(traceback.format_exc())
            raise RuntimeError
