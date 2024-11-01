import logging
import unittest
import os

from unittest.mock import patch

from shared.auxiliary_tools.src.environment_utils import EnvironmentUtils

ENVIRONMENT_VARIABLES = {
    "LOG_LEVEL": "ERROR",
    "TEST_ENVIRONMENT_VARIABLE": "test",
    "TEST_COMMA_SEPARATED_LIST": "test1,test2,test3",
}


class EnvironmentUtilsTest(unittest.TestCase):

    @patch.dict(os.environ, ENVIRONMENT_VARIABLES, clear=True)
    def test_get_logger(self):
        """
        Tests that the logger is returned correctly and the log level is set based on the environment variable.
        """
        logger = EnvironmentUtils.get_logger()

        self.assertIsNotNone(logger)
        self.assertEqual(logging.ERROR, logger.level)

    def test_get_logger_no_level_variable(self):
        """
        Tests that the logger is returned correctly and the log level is set to the default.
        """
        logger = EnvironmentUtils.get_logger()

        self.assertIsNotNone(logger)
        self.assertEqual(logging.INFO, logger.level)
