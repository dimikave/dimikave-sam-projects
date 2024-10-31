import os
import json
import logging

import boto3
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from sendgrid_apod_email_utils import (
    get_greeting_by_day,
    get_title,
    get_url,
    get_explanation,
    calculate_day_counter,
)
from sendgrid_email_templates import generate_email_template
import sendgrid_apod_email_constants as c
from sendgrid_apod_email_enumerations import GPTKeys, S3Keys

# Initialize S3 client
s3 = boto3.client("s3")

# TODO Add shared package for logger and GPT
logger = logging.getLogger(__name__)
# Ensure that the log level is set at the right level (in this case INFO)
logger.setLevel(logging.INFO)

# Add a handler only if none exist (this step may not be required, but it's good practice)
if not logger.handlers:
    handler = logging.StreamHandler()  # Logs to stdout (which Lambda captures and sends to CloudWatch)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def generate_content_from_gpt4(prompt: str, model: str = c.GPT_MODEL, max_tokens: int = 100) -> str:
    """
    Generates content using GPT-4 via a direct API call.

    :param prompt: str: The prompt to send to GPT-4.
    :param model: str: The GPT model to use (default: "gpt-4").
    :param max_tokens: int: Maximum number of tokens to generate (default: 100).

    :return: str: Generated text from GPT-4.

    :raises: Exception: If the API call fails.
    """
    api_key = os.environ[c.OPENAI_API_KEY]
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {
        GPTKeys.MODEL.value: model,
        GPTKeys.MESSAGES.value: [{GPTKeys.ROLE.value: GPTKeys.USER.value, GPTKeys.CONTENT.value: prompt}],
        GPTKeys.MAX_TOKENS.value: max_tokens,
    }

    response = requests.post(url=c.GPT_COMPLETIONS_URL, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()[GPTKeys.CHOICES.value][0][GPTKeys.MESSAGE.value][GPTKeys.CONTENT.value].strip()
    else:
        raise Exception(f"Failed to call OpenAI API: {response.status_code} - {response.text}")


def get_mysterious_content_from_gpt4() -> str:
    """
    Generates mysterious content about space exploration using GPT-4.

    :return: str: Generated mysterious content.
    """
    prompt = "Generate a mysterious and atmospheric description about space exploration and the universe using around 50 words"
    return generate_content_from_gpt4(prompt)


def get_space_fact_from_gpt4() -> str:
    """
    Generates an interesting space fact using GPT-4.

    :return: str: Generated space fact.
    """
    prompt = "Provide an interesting and accurate fact about space or astronomy."
    return generate_content_from_gpt4(prompt)


def get_recipients_from_s3(bucket_name: str, file_key: str) -> list:
    """
    Fetches the recipients list from an S3 file.

    :param bucket_name: str: Name of the S3 bucket.
    :param file_key: str: Key of the file in the S3 bucket.

    :return: list: List of recipient email addresses.
    """
    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        content = response[S3Keys.BODY.value].read().decode(S3Keys.UTF_8.value)
        recipients_data = json.loads(content)
        return recipients_data.get(S3Keys.RECIPIENTS_KEY.value, [])
    except Exception as e:
        logger.info(f"Error fetching recipients from S3: {e}")
        return []


def send_email_sendgrid(sender: str, recipients: list, subject: str, html_body: str) -> bool:
    """
    Sends an email using SendGrid.

    :param sender: str: Sender's email address.
    :param recipients: list: List of recipient email addresses.
    :param subject: str: Email subject.
    :param html_body: str: HTML content of the email.

    :return: bool: True if the email was sent successfully, False otherwise.
    """
    message = Mail(
        from_email=sender,
        to_emails=recipients,
        subject=subject,
        html_content=html_body,
    )

    try:
        sg = SendGridAPIClient(os.environ[c.SENDGRID_API_KEY])
        response = sg.send(message)
        return response.status_code == 202
    except Exception as e:
        logger.error(f"Error sending email via SendGrid: {e}")
        return False


def get_data(api_key: str) -> dict:
    """
    Fetch NASA APOD data using the provided API key.

    :param api_key: str: NASA API key.

    :return: dict: JSON response from the NASA APOD API.
    """
    raw_response = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={api_key}").text

    return json.loads(raw_response)


def lambda_handler(event, context):
    """
    AWS Lambda handler function for sending NASA APOD emails.

    :param event: dict: AWS Lambda event data.
    :param context: object: AWS Lambda context object.

    :returns dict: Response containing statusCode and body.
    """
    try:
        # Get environment variables
        nasa_api_key = os.environ[c.NASA_API_KEY]
        s3_bucket_name = os.environ[c.S3_BUCKET]
        s3_file_key = os.environ[c.S3_FILE_KEY]
        sender = os.environ[c.SENDER_EMAIL]

        # Fetch the recipients list from S3
        recipients = get_recipients_from_s3(s3_bucket_name, s3_file_key)

        logger.info(S3Keys.RECIPIENTS_KEY.value)
        logger.info(recipients)

        # Fetch the APOD data
        apod_data = get_data(nasa_api_key)
        logger.info(apod_data)
        url = get_url(apod_data)
        day_counter = calculate_day_counter()
        greeting = get_greeting_by_day(day_counter)
        title = get_title(apod_data)
        explanation = get_explanation(apod_data)
        mysterious_content = get_mysterious_content_from_gpt4()
        space_fact = get_space_fact_from_gpt4()

        # Prepare email content
        subject = f"Cosmic Journey - Day {day_counter}: Today's NASA Astronomy Picture of the Day!"
        html_body = generate_email_template(greeting, title, url, explanation, mysterious_content, space_fact)

        # Send the email via Sendgrid
        if send_email_sendgrid(sender, recipients, subject, html_body):
            logger.info(c.SUCCESS_RESPONSE)
            return c.SUCCESS_RESPONSE
        else:
            logger.error(c.FAILURE_RESPONSE)
            return c.FAILURE_RESPONSE

    except Exception as e:
        logger.error(f"Error: {e}")
        logger.info(c.FAILURE_RESPONSE)
        return c.FAILURE_RESPONSE
