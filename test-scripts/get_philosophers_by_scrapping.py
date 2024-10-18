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


# import os
# import requests
#
#
# # Function to make a direct HTTP call to the OpenAI API
# def generate_content_from_gpt4(prompt, model="gpt-4", max_tokens=100):
#     """
#     Makes a direct API call to OpenAI using the requests library.
#
#     Args:
#         prompt (str): The prompt to send to GPT-4.
#         model (str): The GPT model to use (e.g., "gpt-4").
#         max_tokens (int): The maximum number of tokens to generate.
#
#     Returns:
#         str: The generated text from GPT-4.
#     """
#     api_key = os.environ["OPENAI_API_KEY"]
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

# print(generate_content_from_gpt4("Hello there"))


# ================================ SOLUTION 1, MANY ======================================

# import requests
# import datetime


# def get_philosopher_by_day():
#     # Fetch ordered philosophers
#     query =
# """
#     SELECT ?philosopher ?philosopherLabel ?birthdate WHERE {
#       ?philosopher wdt:P106 wd:Q4964182;
#                    wdt:P569 ?birthdate.
#       SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
#     }
#     ORDER BY ?philosopher
#     """
#     url = "https://query.wikidata.org/sparql"
#     headers = {"Accept": "application/sparql-results+json"}
#     response = requests.get(url, headers=headers, params={'query': query})
#     data = response.json()
#
#     philosophers = [
#         {
#             "id": item['philosopher']['value'],
#             "name": item['philosopherLabel']['value'],
#             "birthdate": item['birthdate']['value']
#         }
#         for item in data['results']['bindings']
#     ]
#
#     # Get current day of the year (1-365)
#     current_day_of_year = datetime.datetime.now().timetuple().tm_yday
#     print(len(philosophers))
#     # Use modulo to cycle through philosophers
#     index = current_day_of_year-1 % len(philosophers)
#     return philosophers[index]

# # Example Usage
# philosopher_of_the_day = get_philosopher_by_day()
# print(f"Philosopher of the Day: {philosopher_of_the_day['name']} (Born: {philosopher_of_the_day['birthdate']})")


# ================================ SITE 2 ======================================
import requests
from bs4 import BeautifulSoup
import json
import boto3

# Initialize S3 client
s3 = boto3.client('s3')


def get_famous_philosophers_names():
    """
    Scrapes the names of philosophers from the website and returns them as a list.
    """
    url = "https://www.famousphilosophers.org/list/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <tr> elements, which contain philosopher information
        philosopher_rows = soup.find_all('tr')

        philosopher_names = []

        # Loop through each row and extract the philosopher's name
        for row in philosopher_rows:
            columns = row.find_all('td')
            if len(columns) == 4:  # Ensure the row has all the expected columns
                name = columns[0].find('a').text  # Name in the first column
                philosopher_names.append(name)

        return philosopher_names
    else:
        print(f"Failed to retrieve the page: {response.status_code}")
        return []


def save_names_to_json_and_upload(names, s3_bucket, s3_key):
    """
    Saves the list of philosopher names to a JSON file and uploads it to S3.
    """
    # Convert the names to JSON format
    json_data = json.dumps(names, indent=4)

    # Save the JSON data to a local file
    with open('philosophers.json', 'w') as f:
        f.write(json_data)


# Example usage
philosopher_names = get_famous_philosophers_names()

# Define your S3 bucket and file key (path in S3)
s3_bucket = 'philosophy'
s3_key = 'philosophers.json'

# Save the names to JSON and upload to S3
save_names_to_json_and_upload(philosopher_names, s3_bucket, s3_key)


#
# def get_lafave_philosophers():
#     url = "https://lafavephilosophy.x10host.com/CRONLIST.htm"
#     start_time = time.time()
#
#     response = requests.get(url)
#
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#
#         # Find all <tr> elements, which contain philosopher information
#         philosopher_rows = soup.find_all('tr')
#
#         philosophers = []
#
#         # Loop through each row and extract relevant details
#         for row in philosopher_rows:
#             columns = row.find_all('td')
#             if len(columns) == 2:  # Ensure the row has both name and dates
#                 name = columns[0].text.strip()  # Name in the first column (width 60%)
#                 dates = columns[1].text.strip()  # Dates in the second column (width 40%)
#
#                 philosophers.append({
#                     "name": name,
#                     "dates": dates
#                 })
#                 # Stop timing here
#         end_time = time.time()
#
#         # Calculate elapsed time
#         elapsed_time = end_time - start_time
#         print(f"Scraping took {elapsed_time:.2f} seconds")
#         return philosophers
#     else:
#         print(f"Failed to retrieve the page: {response.status_code}")
#         return []
#
#
# # Example usage:
# philosophers = get_lafave_philosophers()
# print(len(philosophers))
#
# # Print the first 10 philosophers
# # for philosopher in philosophers:
# #     print(f"Name: {philosopher['name']}")
# # #     print(f"Dates: {philosopher['dates']}")
# #     print("---")
