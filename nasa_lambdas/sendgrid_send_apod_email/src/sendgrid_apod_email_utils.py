from datetime import datetime
import boto3
from sendgrid_apod_email_enumerations import APODResponseKeys
import sendgrid_apod_email_constants as c

# Initialize S3 client
s3 = boto3.client("s3")


def get_greeting_by_day(day_count: int) -> str:
    """
    Get a greeting based on the day counter.

    :param day_count: int: The current day count
    :return: str: A greeting from the predefined list
    """
    index: int = (day_count - 1) % len(c.GREETINGS_LIST)
    return c.GREETINGS_LIST[index]


def calculate_day_counter() -> int:
    """
    Calculate the number of days since a fixed start date.

    :return: int: The number of days since October 17, 2024
    """
    start_date: datetime = datetime(2024, 10, 17)
    current_date: datetime = datetime.now()
    day_count: int = (current_date - start_date).days + 1
    return day_count


def get_title(response: dict[str, str]) -> str:
    """
    Extract the title from the NASA APOD response.

    :param response: dict[str, str]: NASA APOD API response
    :return: str: Title of the APOD
    """
    return response[APODResponseKeys.TITLE.value]


def get_url(response: dict[str, str]) -> str:
    """
    Extract the image URL from the NASA APOD response.

    :param response: dict[str, str]: NASA APOD API response
    :return: str: URL of the APOD image
    """
    return response[APODResponseKeys.URL.value]


def get_explanation(response: dict[str, str]) -> str:
    """
    Extract the explanation from the NASA APOD response.

    :param response: dict[str, str]: NASA APOD API response
    :return: str: Explanation of the APOD
    """
    return response[APODResponseKeys.EXPLANATION.value]
