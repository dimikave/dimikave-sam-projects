import os
import requests
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
#
#
#
# # Get environment variables
# OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
# SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY"]
# SENDER_EMAIL = os.environ["SENDER_EMAIL"]
# RECIPIENT_EMAIL = [SENDER_EMAIL]
#
#
# def generate_content_from_gpt4(prompt, model="gpt-4o-mini", max_tokens=500):
#     api_key = OPENAI_API_KEY
#     headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
#     data = {"model": model, "messages": [{"role": "user", "content": prompt}], "max_tokens": max_tokens}
#
#     # Make the HTTP request to OpenAI API
#     response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
#
#     if response.status_code == 200:
#         return response.json()["choices"][0]["message"]["content"].strip()
#     else:
#         raise Exception(f"Failed to call OpenAI API: {response.status_code} - {response.text}")
def generate_content_from_gpt4(prompt, model="gpt-4o-mini", max_tokens=100):
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
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens
    }

    # Make the HTTP request to OpenAI API
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        raise Exception(f"Failed to call OpenAI API: {response.status_code} - {response.text}")

print(generate_content_from_gpt4("Hello"))
#
# def generate_email_content(philosopher_name):
#     # Generate content using OpenAI API
#     summary = generate_content_from_gpt4(f"Provide a concise summary of the philosophy of {philosopher_name} in 5-6 sentences.")
#
#     # Fetch Key Concepts as an HTML ordered list
#     key_concepts = generate_content_from_gpt4(
#         f"List the key concepts of {philosopher_name}'s philosophy (and a few words for each) as an HTML ordered list (<ol> and <li> tags).")
#
#     # Fetch Food for Thought as an HTML ordered list
#     food_for_thought = generate_content_from_gpt4(
#         f"Provide 5 complex (challenging) questions stemming from {philosopher_name}'s philosophy as an HTML ordered list (<ol> and <li> tags). Food for thought.")
#
#     # Load HTML template (use the updated Earthy Wisdom template provided above)
#     html_template = """
#     <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Philosopher's Daily Reflection</title>
#     <style>
#         body {
#             font-family: 'Palatino Linotype', 'Book Antiqua', Palatino, serif;
#             background-color: #f4f1de;
#             color: #333;
#             margin: 0;
#             padding: 0;
#         }
#         .container {
#             max-width: 800px;
#             margin: 20px auto;
#             background: #fefae0;
#             padding: 20px;
#             border-radius: 10px;
#             box-shadow: 0 4px 8px rgba(0,0,0,0.1);
#             border: 1px solid #d4a373;
#         }
#         h1 {
#             color: #bc6c25;
#             font-size: 28px;
#             text-align: center;
#             padding-bottom: 10px;
#             border-bottom: 2px solid #bc6c25;
#         }
#         h2 {
#             color: #606c38;
#             font-size: 22px;
#             margin-top: 20px;
#             margin-bottom: 10px;
#             text-align: left;
#         }
#         h3 {
#             color: #283618;
#             font-size: 20px;
#             margin-top: 20px;
#             margin-bottom: 10px;
#         }
#         p, ol, ul {
#             line-height: 1.8;
#             font-size: 16px;
#             color: #333;
#         }
#         ol, ul {
#             padding-left: 30px;
#         }
#         .summary, .key-concepts, .thoughts {
#             background: #e9edc9;
#             padding: 15px;
#             border-left: 5px solid #606c38;
#             margin-top: 20px;
#             border-radius: 8px;
#         }
#         .key-concepts {
#             background: #d4e09b;
#         }
#         .thoughts {
#             background: #faedcd;
#             margin-top: 40px;  /* Added spacing between thoughts and key concepts */
#         }
#         .footer {
#             text-align: center;
#             margin-top: 40px;
#             font-size: 14px;
#             color: #6c757d;
#         }
#     </style>
# </head>
# <body>
#     <div class="container">
#         <h1>Philosopher of the Day: {{philosopher_name}}</h1>
#         <div class="summary">
#             <h3>Overview - Summary</h3>
#             <p>{{philosopher_summary}}</p>
#         </div>
#
#         <div class="key-concepts">
#             <h3>Key Concepts</h3>
#             {{key_concepts}}
#         </div>
#
#         <div class="thoughts">
#             <h3>Food for Thought</h3>
#             {{food_for_thought}}
#         </div>
#
#         <div class="footer">
#             <p>Brought to you by your favorite casual think-ass cool guy Dimi Kave!</p>
#         </div>
#     </div>
# </body>
# </html>
#     """
#
#     # Replace placeholders in the HTML template with actual content
#     html_content = html_template.replace('{{philosopher_name}}', philosopher_name)
#     html_content = html_content.replace('{{philosopher_summary}}', summary)
#     html_content = html_content.replace('{{key_concepts}}', key_concepts)
#     html_content = html_content.replace('{{food_for_thought}}', food_for_thought)
#
#     return html_content
#
# def send_test_email(philosopher_name):
#     # Generate the email content
#     email_content = generate_email_content(philosopher_name)
#
#     print(email_content)
#
#     # Create the email message
#     message = Mail(
#         from_email=SENDER_EMAIL,
#         to_emails=RECIPIENT_EMAIL,
#         subject=f"Philosopher's Daily Reflection: {philosopher_name}",
#         html_content=email_content
#     )
#
#     try:
#         sg = SendGridAPIClient(SENDGRID_API_KEY)
#         response = sg.send(message)
#         print(f"Email sent to {RECIPIENT_EMAIL}: {response.status_code}")
#     except Exception as e:
#         print(f"Error sending email: {e}")
#
#
# if __name__ == "__main__":
#     # Replace 'Aristotle' with the philosopher you want to test with
#     send_test_email('John Locke')