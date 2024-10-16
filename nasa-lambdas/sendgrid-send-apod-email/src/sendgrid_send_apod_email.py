import os
import json
from datetime import datetime
import requests

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Predefined list of greetings
greetings_list = [
    "Greetings, Cosmic Explorer!",
    "Hello, Star Traveler!",
    "Dear Astral Adventurer!",
    "Welcome, Space Enthusiast!",
    "Salutations, Celestial Voyager!",
    "Hi, Galactic Traveler!",
    "Hello, Cosmic Wanderer!",
    "Greetings, Interstellar Dreamer!",
    "Welcome, Universe Seeker!",
    "Salutations, Orbiting Observer!"
]

# Function to get the greeting based on the day counter
def get_greeting_by_day(day_count):
    index = (day_count - 1) % len(greetings_list)  # Using day_count - 1 for 0-based index
    return greetings_list[index]

# Function to calculate the day counter
def calculate_day_counter():
    start_date = datetime(2024, 10, 17)
    current_date = datetime.now()
    day_count = (current_date - start_date).days + 1  # +1 to start counting from Day 1
    return day_count

# Function to generate mysterious content
def get_mysterious_content():
    return (
        "As you gaze upon today’s cosmic masterpiece, ponder the vastness of our universe. "
        "Did you know that there are more stars in the universe than grains of sand on all the beaches on Earth? "
        "The mysteries of space are endless, and each image unveils a story waiting to be discovered."
    )

# Function to generate a space fact
def get_space_fact():
    return (
        "Did you know? A day on Venus is longer than a year on Venus! "
        "It takes 243 Earth days to rotate once on its axis but only 225 Earth days to complete an orbit around the Sun."
    )

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


# Function to generate the email HTML template
def generate_email_template(greeting, title, url, explanation, mysterious_content, space_fact):
    """Generate an HTML email template for NASA's APOD."""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NASA's Astronomy Picture of the Day</title>
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #0a0a2a; color: #ffffff;">
    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; margin: 0 auto; background-color: #1a1a4a;">
        <tr>
            <td style="padding: 20px; text-align: center; background-color: #1a237e;">
                <h1 style="margin: 0; font-size: 24px; color: #ffffff;">NASA's Astronomy Picture of the Day</h1>
            </td>
        </tr>
        <tr>
            <td style="padding: 20px;">
                <h2 style="color: #ffffff;">{greeting}</h2>
                <h3 style="color: #00ffff;">{title}</h3>
                <img src="{url}" alt="{title}" style="max-width: 100%; height: auto; border-radius: 8px; margin-bottom: 15px;">
                <p style="color: #af2f6f;">{mysterious_content}</p>
                <div style="background-color: #2a2a6a; border-left: 4px solid #00ffff; padding: 15px; margin: 15px 0;">
                <strong style="color: #00ffff;">Picture of the day description:</strong>
                 <span style="color: #ffffff;">{explanation}</span>
                </div>
                <div style="background-color: #2a2a6a; border-left: 4px solid #00ffff; padding: 15px; margin: 15px 0;">
                    <strong style="color: #00ffff;">Fact of the Day:</strong> 
                    <span style="color: #ffffff;">{space_fact}</span>
                </div>
                <p style="color: #ffffff;">Embark on this cosmic journey and find the image history on <a href="https://apod.nasa.gov/apod/archivepix.html" style="color: #00ffff; text-decoration: none;">NASA APOD archive</a>.</p>
            </td>
        </tr>
        <tr>
            <td style="padding: 20px; text-align: center; background-color: #1a237e; color: #ffffff;">
                <p style="margin: 0; font-size: 14px;">&copy; Brought to you by your cosmic white nigga Dimitris Kavelidis</p>
            </td>
        </tr>
    </table>
</body>
</html>
"""

# Function to send an email using SES
def send_email_sendgrid(sender, recipients, subject, html_body):
    """Send an email using SendGrid."""
    message = Mail(
        from_email=sender,
        to_emails=recipients,
        subject=subject,
        html_content=html_body,
    )

    sg = SendGridAPIClient(os.environ["SENDGRID_API_KEY"])
    response = sg.send(message)
    return response


# Lambda handler function
def lambda_handler(event, context):
    try:
        # Get the NASA API key from environment variables
        nasa_api_key = os.environ['NASA_API_KEY']

        if event['recipients']:
            recipients = event['recipients']  # A list of email addresses
        else:
            # Get the list of recipients from the event object
            recipients = os.environ['RECIPIENTS'].split(',')  # Converts string to list


        # Fetch the APOD data
        apod_data = get_data(nasa_api_key)
        url = get_url(apod_data)
        day_counter = calculate_day_counter()
        greeting = get_greeting_by_day(day_counter)
        title = get_title(apod_data)
        explanation = get_explanation(apod_data)
        mysterious_content = get_mysterious_content()
        space_fact = get_space_fact()

        # Prepare email content
        sender = os.environ['SENDER_EMAIL']  # Sender email must be verified in SES
        subject = f"Cosmic Journey - Day {day_counter}: Today's NASA Astronomy Picture of the Day!"

        # Prepare email content using the HTML template
        html_body = generate_email_template(greeting, title, url, explanation, mysterious_content, space_fact)
        # Send the email via SES
        if send_email_sendgrid(sender, recipients, subject, html_body):
            return {
                'statusCode': 200,
                'body': json.dumps('Emails sent successfully!')
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps('Failed to send emails')
            }

    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {e}")
        }

