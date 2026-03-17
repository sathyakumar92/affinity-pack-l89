import logging
import json
from pathlib import Path
from typing import Optional
import win32com.client

class AffinityDesignerClient:
    """
    A client interface for interacting with Affinity Designer for Windows.

    This class provides methods to connect to the Affinity Designer application,
    check if it is installed, retrieve the version, and disconnect from the application.
    """

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initializes the AffinityDesignerClient.

        :param config_path: Optional path to a JSON configuration file for client settings.
        """
        self.config_path = config_path
        self.app = None
        self.logger = self.setup_logging()

        if self.config_path:
            self.load_config()

    def setup_logging(self) -> logging.Logger:
        """
        Sets up logging for the client.

        :return: Configured logger instance.
        """
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        return logging.getLogger(__name__)

    def load_config(self):
        """
        Loads configuration from the specified JSON file.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            json.JSONDecodeError: If the configuration file contains invalid JSON.
        """
        if not self.config_path.is_file():
            self.logger.error(f"Configuration file not found: {self.config_path}")
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        with open(self.config_path, 'r') as file:
            try:
                config = json.load(file)
                self.logger.info("Configuration loaded successfully.")
            except json.JSONDecodeError as e:
                self.logger.error(f"Error decoding JSON from configuration file: {e}")
                raise

    def connect(self) -> bool:
        """
        Connects to the Affinity Designer application.

        :return: True if the connection is successful, False otherwise.
        """
        try:
            self.app = win32com.client.Dispatch("Affinity.Designer")
            self.logger.info("Connected to Affinity Designer.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect to Affinity Designer: {e}")
            return False

    def disconnect(self):
        """
        Disconnects from the Affinity Designer application.
        """
        if self.app:
            self.logger.info("Disconnecting from Affinity Designer.")
            self.app = None
        else:
            self.logger.warning("No active connection to disconnect.")

    def get_version(self) -> str:
        """
        Retrieves the version of the Affinity Designer application.

        :return: Version string of the application.
        :raises Exception: If the application is not connected.
        """
        if not self.app:
            self.logger.error("Attempted to get version while not connected.")
            raise Exception("Not connected to Affinity Designer.")

        version = self.app.Version  # Assuming the COM object has a Version property
        self.logger.info(f"Retrieved version: {version}")
        return version

    def is_installed(self) -> bool:
        """
        Checks if Affinity Designer is installed on the system.

        :return: True if installed, False otherwise.
        """
        try:
            win32com.client.Dispatch("Affinity.Designer")
            self.logger.info("Affinity Designer is installed.")
            return True
        except Exception:
            self.logger.info("Affinity Designer is not installed.")
            return False
