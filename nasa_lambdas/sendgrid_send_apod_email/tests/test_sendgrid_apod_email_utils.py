import unittest
from datetime import datetime, timedelta
from freezegun import freeze_time
from parameterized import parameterized
from unittest.mock import patch
from nasa_lambdas.sendgrid_send_apod_email.tests.data_providers.input_providers import (
    greeting_provider,
    title_extraction_provider,
    url_extraction_provider,
    explanation_extraction_provider,
)
from nasa_lambdas.sendgrid_send_apod_email.src.sendgrid_apod_email_utils import (
    get_greeting_by_day,
    calculate_day_counter,
    get_title,
    get_url,
    get_explanation,
)


class TestSendGridAPODEmailFunctions(unittest.TestCase):

    @parameterized.expand(greeting_provider)
    @patch(
        "sendgrid_apod_email_constants.GREETINGS_LIST", ["Hello, Earth!", "Hi from beyond!", "Greetings from space!"]
    )
    def test_get_greeting_by_day(self, day_count: int, expected_greeting: str) -> None:
        """
        Tests get_greeting_by_day function.
        """
        result = get_greeting_by_day(day_count)
        self.assertEqual(expected_greeting, result)

    def test_calculate_day_counter(self) -> None:
        """
        Tests calculate_day_counter function by freezing the current date to a specific point in time.
        """
        # Define the start date and the target frozen date (10 days after start_date)
        start_date = datetime(2024, 10, 17)
        frozen_date = start_date + timedelta(days=10)

        # Freeze time to the frozen date
        with freeze_time(frozen_date):
            result = calculate_day_counter()

        # Assert that the result is 11 (10 days after start_date + 1)
        self.assertEqual(result, 11)

    @parameterized.expand(title_extraction_provider)
    def test_get_title(self, response: dict[str, str], expected_title: str) -> None:
        """
        Tests get_title function with various responses.
        """
        result = get_title(response)
        self.assertEqual(expected_title, result)

    @parameterized.expand(url_extraction_provider)
    def test_get_url(self, response: dict[str, str], expected_url: str) -> None:
        """
        Tests get_url function with various responses.
        """
        result = get_url(response)
        self.assertEqual(expected_url, result)

    @parameterized.expand(explanation_extraction_provider)
    def test_get_explanation(self, response: dict[str, str], expected_explanation: str) -> None:
        """
        Tests get_explanation function with various explanations.
        """
        result = get_explanation(response)
        self.assertEqual(result, expected_explanation)
