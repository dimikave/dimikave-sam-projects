import os
import json
import random
from datetime import datetime

import boto3
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from auxiliary_tools.environment_utils import EnvironmentUtils

# Initialize S3 client
s3 = boto3.client("s3")
logger = EnvironmentUtils.get_logger()


# Function to calculate the day counter starting from 2024-10-17
def calculate_day_counter():
    start_date = datetime(2024, 10, 18)
    current_date = datetime.now()
    return (current_date - start_date).days + 1  # Start from Day 1


# Function to make a direct HTTP call to the OpenAI API
def generate_content_from_gpt4(prompt, model="gpt-4o-mini", max_tokens=500):
    """
    Makes a direct API call to OpenAI using the requests library.

    Args:
        prompt (str): The prompt to send to GPT-4.
        model (str): The GPT model to use (e.g., "gpt-4").
        max_tokens (int): The maximum number of tokens to generate.

    Returns:
        str: The generated text from GPT-4.
    """
    api_key = os.environ["OPENAI_API_KEY"]
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"model": model, "messages": [{"role": "user", "content": prompt}], "max_tokens": max_tokens}

    # Make the HTTP request to OpenAI API
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        raise Exception(f"Failed to call OpenAI API: {response.status_code} - {response.text}")


# Function to generate email content about a philosopher using OpenAI
def generate_email_content(philosopher_list):
    # Chose a philosopher randomly.
    philosopher_name = random.choice(philosopher_list)
    # Generate content using OpenAI API
    summary = generate_content_from_gpt4(
        f"Provide a concise summary of the philosophy of {philosopher_name} in 5-6 sentences."
    )

    # Fetch Key Concepts as an HTML ordered list
    key_concepts = generate_content_from_gpt4(
        f"List the key concepts of {philosopher_name}'s philosophy (and a few words for each) as an HTML ordered list (<ol> and <li> tags). Answer strictly ONLY with the list."
    )

    # Fetch Food for Thought as an HTML ordered list
    food_for_thought = generate_content_from_gpt4(
        f"Provide 5 complex (challenging-food for thought) questions stemming from {philosopher_name}'s philosophy as an HTML ordered list (<ol> and <li> tags). Answer strictly ONLY with the list."
    )

    # Load HTML template (use the updated Earthy Wisdom template provided above)
    html_template = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Philosopher's Daily Reflection</title>
    <style>
        body {
            font-family: 'Palatino Linotype', 'Book Antiqua', Palatino, serif;
            background-color: #f4f1de;
            color: #333;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 800px;
            margin: 20px auto;
            background: #fefae0;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            border: 1px solid #d4a373;
        }
        h1 {
            color: #bc6c25;
            font-size: 28px;
            text-align: center;
            padding-bottom: 10px;
            border-bottom: 2px solid #bc6c25;
        }
        h2 {
            color: #606c38;
            font-size: 22px;
            margin-top: 20px;
            margin-bottom: 10px;
            text-align: left;
        }
        h3 {
            color: #283618;
            font-size: 20px;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        p, ol, ul {
            line-height: 1.8;
            font-size: 16px;
            color: #333;
        }
        ol, ul {
            padding-left: 30px;
        }
        .summary, .key-concepts, .thoughts {
            background: #e9edc9;
            padding: 15px;
            border-left: 5px solid #606c38;
            margin-top: 20px;
            border-radius: 8px;
        }
        .key-concepts {
            background: #d4e09b;
        }
        .thoughts {
            background: #faedcd;
            margin-top: 40px;  /* Added spacing between thoughts and key concepts */
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            font-size: 14px;
            color: #6c757d;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Philosopher of the Day: {{philosopher_name}}</h1>
        <div class="summary">
            <h3>Overview - Summary</h3>
            <p>{{philosopher_summary}}</p>
        </div>

        <div class="key-concepts">
            <h3>Key Concepts</h3>
            {{key_concepts}}
        </div>

        <div class="thoughts">
            <h3>Food for Thought</h3>
            {{food_for_thought}}
        </div>

        <div class="footer">
            <p>Brought to you by your favorite casual think-ass cool guy Dimi Kave!</p>
        </div>
    </div>
</body>
</html>
    """

    # Replace placeholders in the HTML template with actual content
    html_content = html_template.replace("{{philosopher_name}}", philosopher_name)
    html_content = html_content.replace("{{philosopher_summary}}", summary)
    html_content = html_content.replace("{{key_concepts}}", key_concepts)
    html_content = html_content.replace("{{food_for_thought}}", food_for_thought)

    return html_content, philosopher_name


# Function to fetch data from S3
def fetch_from_s3(bucket_name, file_key):
    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        return json.loads(response["Body"].read().decode("utf-8"))
    except Exception as e:
        logger.error(f"Error fetching data from S3: {e}")
        raise


# Function to update data in S3
def update_in_s3(bucket_name, file_key, data):
    try:
        s3.put_object(Bucket=bucket_name, Key=file_key, Body=json.dumps(data), ContentType="application/json")
    except Exception as e:
        logger.error(f"Error updating data in S3: {e}")
        raise


# Function to send an email using Sendgrid
def send_email_sendgrid(sender, recipients, subject, html_body):
    message = Mail(
        from_email=sender,
        to_emails=recipients,
        subject=subject,
        html_content=html_body,
    )
    sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
    try:
        response = sg.send(message)
        return response.status_code == 202  # Return True if the email was sent successfully
    except Exception as e:
        logger.error(f"Failed to send email via SendGrid: {e}")
        return False


# Lambda handler function
def lambda_handler(event, context):
    try:
        # Get environment variables
        s3_recipients_bucket_name = os.environ["S3_RECIPIENTS_BUCKET"]
        s3_recipients_file_key = os.environ["S3_RECIPIENTS_FILE_KEY"]
        s3_philosophers_bucket_name = os.environ["S3_PHILOSOPHERS_BUCKET"]
        s3_philosophers_file_key = os.environ["S3_PHILOSOPHERS_FILE_KEY"]
        sender = os.environ["SENDER_EMAIL"]

        # Fetch recipients and philosophers from S3
        recipients_data = fetch_from_s3(s3_recipients_bucket_name, s3_recipients_file_key)
        philosophers_data = fetch_from_s3(s3_philosophers_bucket_name, s3_philosophers_file_key)

        recipients = recipients_data.get("recipients", [])
        philosophers = philosophers_data.get("philosophers", [])

        if not recipients:
            logger.warning("No recipients found.")
            return {"statusCode": 400, "body": json.dumps("No recipients found")}

        if not philosophers:
            logger.warning("No philosophers found.")
            return {"statusCode": 400, "body": json.dumps("No philosophers found")}

        # Generate email content and get the philosopher
        content, philosopher = generate_email_content(philosophers)
        day_counter = calculate_day_counter()
        subject = f"Philosopher's Daily Reflection - Day {day_counter}: Philosopher of the Day is ... !"

        # Send the email via SendGrid
        if send_email_sendgrid(sender, recipients, subject, content):
            # Remove the philosopher from the list and update S3 after successful email
            logger.info("Email sent. Removing philosopher from s3 bucket...")
            philosophers.remove(philosopher)
            update_in_s3(s3_philosophers_bucket_name, s3_philosophers_file_key, {"philosophers": philosophers})
            logger.info("Philosopher removed.")
            return {"statusCode": 200, "body": json.dumps("Emails sent and philosopher removed successfully!")}
        else:
            return {"statusCode": 500, "body": json.dumps("Failed to send emails")}

    except Exception as e:
        logger.error(f"Error: {e}")
        return {"statusCode": 500, "body": json.dumps(f"Error: {e}")}
