import os

from logging import Logger, getLogger

from .environment_constants import EnvironmentConstants

class EnvironmentUtils:
    """
    Utility methods for the environment of lambdas.
    """

    @staticmethod
    def get_logger() -> Logger:
        """
        Returns a logger that can be used for the logging in lambda functions.

        :return: Logger: A logger object
        """
        log_level = os.environ.get(EnvironmentConstants.LOG_LEVEL,EnvironmentConstants.LOG_LEVEL_DEFAULT)
        logger = getLogger()
        logger.setLevel(log_level)

        return logger
