# from openai import OpenAI
# client = OpenAI()
#
# stream = client.chat.completions.create(
#     model="gpt-4",
#     messages=[{"role": "user", "content": "Fact of the day for space"}],
#     stream=True,
#     max_completion_tokens=100,
# )
# for chunk in stream:
#     print(chunk.choices[0].delta.content or "", end="")


import os
import requests


# Function to make a direct HTTP call to the OpenAI API
def generate_content_from_gpt4(prompt, model="gpt-4", max_tokens=100):
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


print(generate_content_from_gpt4("Hello there"))
