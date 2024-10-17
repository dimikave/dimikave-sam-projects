import os
import json
import requests
import boto3
from botocore.exceptions import ClientError


# Function to get NASA APOD data
def get_data(api_key):
    raw_response = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={api_key}").text
    response = json.loads(raw_response)
    return response


# Function to extract title, url, and explanation
def get_title(response):
    return response["title"]


def get_url(response):
    return response["url"]


def get_explanation(response):
    return response["explanation"]


# Function to send an email using SES
def send_email_ses(sender, recipients, subject, html_body):
    # Initialize boto3 client for SES
    ses_client = boto3.client("ses", region_name="eu-west-1")

    try:
        # Send email
        response = ses_client.send_email(
            Source=sender,
            Destination={"ToAddresses": recipients},  # List of recipients
            Message={
                "Subject": {
                    "Data": subject,
                },
                "Body": {
                    "Html": {
                        "Data": html_body,
                    }
                },
            },
        )
        print(f"Email sent! Message ID: {response['MessageId']}")
    except ClientError as e:
        print(f"Error: {e.response['Error']['Message']}")
        return False
    return True


# Lambda handler function
def lambda_handler(event, context):
    try:
        # Get the NASA API key from environment variables
        nasa_api_key = os.environ["NASA_API_KEY"]

        if event["recipients"]:
            recipients = event["recipients"]  # A list of email addresses
        else:
            # Get the list of recipients from the event object
            recipients = os.environ["RECIPIENTS"].split(",")  # Converts string to list

        # Fetch the APOD data
        apod_data = get_data(nasa_api_key)
        url = get_url(apod_data)
        title = get_title(apod_data)
        explanation = get_explanation(apod_data)

        # Prepare email content
        sender = os.environ["SENDER_EMAIL"]  # Sender email must be verified in SES
        subject = f"NASA APOD: {title}"
        html_body = f'<h1>{title}</h1><img src="{url}" alt="{title}" style="max-width: 100%;"/><p>{explanation}</p>'

        # Send the email via SES
        if send_email_ses(sender, recipients, subject, html_body):
            return {"statusCode": 200, "body": json.dumps("Emails sent successfully!")}
        else:
            return {"statusCode": 500, "body": json.dumps("Failed to send emails")}

    except Exception as e:
        print(f"Error: {e}")
        return {"statusCode": 500, "body": json.dumps(f"Error: {e}")}
