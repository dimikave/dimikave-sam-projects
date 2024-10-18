# Predefined list of greetings
import json

GREETINGS_LIST = [
    "Greetings, Cosmic Explorer!",
    "Hello, Star Traveler!",
    "Dear Astral Adventurer!",
    "Welcome, Space Enthusiast!",
    "Salutations, Celestial Voyager!",
    "Hi, Galactic Traveler!",
    "Hello, Cosmic Wanderer!",
    "Greetings, Interstellar Dreamer!",
    "Welcome, Universe Seeker!",
    "Salutations, Orbiting Observer!",
]

# Environment Keys
OPENAI_API_KEY = "OPENAI_API_KEY"
SENDGRID_API_KEY = "SENDGRID_API_KEY"
NASA_API_KEY = "NASA_API_KEY"
S3_BUCKET = "S3_BUCKET"
S3_FILE_KEY = "S3_FILE_KEY"
SENDER_EMAIL = "SENDER_EMAIL"

# Response messages
SUCCESS_RESPONSE = {"statusCode": 200, "body": json.dumps("Emails sent successfully!")}
FAILURE_RESPONSE = {"statusCode": 500, "body": json.dumps("Failed to send emails")}


# GPT URL:
GPT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"

# GPT MODEL:
GPT_MODEL = "gpt-4"
