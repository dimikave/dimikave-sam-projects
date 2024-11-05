import os
import requests
import logging
from datetime import datetime, timedelta

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Load environment variables
INSTAGRAM_ACC_ID = os.environ["INSTAGRAM_ACC_ID"]
ACCESS_TOKEN = os.environ["VERIFY_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Define the time threshold (15 minutes ago)
TIME_THRESHOLD = timedelta(minutes=int(os.environ["TIME_THRESHOLD"]))


def lambda_handler(event, context):
    try:
        account_info = fetch_own_account_info()
        own_user_username = account_info["username"]

        # Step 1: Fetch recent media IDs
        media_ids = fetch_instagram_media_ids_with_caption()
        if not media_ids:
            logger.info("No media found.")
            return {"statusCode": 200, "body": "No media found."}

        # Step 2: Fetch comments for each media ID
        for media in media_ids:
            media_id = media["id"]
            comments = fetch_comments_for_media(media_id)
            caption = media["caption"]
            for comment in comments:

                # Skip comments from your own user ID
                if comment["username"] == account_info["username"]:
                    logger.info(f"Skipping comment from own account (User: {own_user_username}): {comment['id']}")
                    continue

                # Step 3: Filter comments within the 15-minute window
                if is_recent_comment(comment["timestamp"]):
                    # Step 4: Generate a response using ChatGPT
                    response_text = generate_content_from_gpt4(f"This photo's caption: {caption}. Respond to user's comment:{comment["text"]}")

                    # Step 5: Post response to Instagram
                    post_instagram_comment_reply(comment["id"], response_text)

        return {"statusCode": 200, "body": "Comments processed successfully."}

    except Exception as e:
        logger.error(f"Error processing comments: {e}")
        return {"statusCode": 500, "body": "Error processing comments"}


def fetch_own_account_info():
    """
    Retrieves the Instagram account ID and username for the authenticated user.

    Returns:
        dict: A dictionary with 'id' and 'username' of the account.
    """
    url = f"https://graph.facebook.com/v21.0/{INSTAGRAM_ACC_ID}?fields=id,username&access_token={ACCESS_TOKEN}"
    response = requests.get(url)
    data = response.json()
    if "id" in data and "username" in data:
        return {"id": data["id"], "username": data["username"]}
    else:
        raise Exception(f"Failed to retrieve account info: {response.text}")


def fetch_instagram_media_ids_with_caption():
    url = f"https://graph.facebook.com/v21.0/{INSTAGRAM_ACC_ID}/media?access_token={ACCESS_TOKEN}&fields=id,caption"
    response = requests.get(url)
    data = response.json()
    return [{"id": item["id"], "caption": item.get("caption", "")} for item in data.get("data", [])]


def is_recent_comment(comment_timestamp):
    # Convert the timestamp from the comment to a datetime object
    comment_time = datetime.strptime(comment_timestamp, "%Y-%m-%dT%H:%M:%S%z")
    # Get the current time in UTC
    now = datetime.now(comment_time.tzinfo)
    # Check if the comment is within the last 15 minutes
    return now - comment_time <= TIME_THRESHOLD


# Function to make a direct HTTP call to the OpenAI API
def generate_content_from_gpt4(prompt, model="gpt-4o-mini", max_tokens=60):
    """
    Makes a direct API call to OpenAI using the requests' library.

    Args:
        prompt (str): The prompt to send to GPT-4.
        model (str): The GPT model to use (e.g., "gpt-4").
        max_tokens (int): The maximum number of tokens to generate.

    Returns:
        str: The generated text from GPT-4.
    """
    api_key = OPENAI_API_KEY
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    messages = [
        {
            "role": "system",
            "content": "You are my social media manager. I need you to reply to social media comments as if you are a space enthousiast who posts daily NASA Astronomy Pictures of the Day (APOD). You respond to comments from followers. If someone asks a question about space or astronomy, provide an informative, friendly response. If the comment is a compliment or casual interaction, keep your reply short, positive, and engaging. Your goal is to gain more followers who are space enthousiasts. Not more than 40 words",
        },
        {"role": "user", "content": prompt},
    ]
    data = {"model": model, "messages": messages, "max_tokens": max_tokens}

    # Make the HTTP request to OpenAI API
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        raise Exception(f"Failed to call OpenAI API: {response.status_code} - {response.text}")


def post_instagram_comment_reply(comment_id, response_text):
    url = f"https://graph.facebook.com/v21.0/{comment_id}/replies"
    payload = {"message": response_text, "access_token": ACCESS_TOKEN}
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        logger.info(f"Replied to comment {comment_id} with: {response_text}")
    else:
        logger.error(f"Failed to reply to comment {comment_id}: {response.text}")


def fetch_comments_for_media(media_id):
    """
    Retrieves top-level comments for a given media item and their replies.
    """
    url = f"https://graph.facebook.com/v21.0/{media_id}/comments?access_token={ACCESS_TOKEN}&fields=id,text,username,timestamp&limit=10"
    response = requests.get(url)
    data = response.json()
    comments = data.get("data", [])

    # Iterate over each top-level comment to fetch replies if they exist
    all_comments = []
    for comment in comments:
        all_comments.append(comment)  # Add top-level comment
        # Fetch replies for the top-level comment
        replies = fetch_replies_for_comment(comment["id"])
        all_comments.extend(replies)  # Add replies to the list

    return all_comments


def fetch_replies_for_comment(comment_id):
    """
    Retrieves replies for a specific comment.
    """
    url = f"https://graph.facebook.com/v21.0/{comment_id}/replies?access_token={ACCESS_TOKEN}&fields=id,text,username,timestamp&limit=5"
    response = requests.get(url)
    data = response.json()
    return data.get("data", [])