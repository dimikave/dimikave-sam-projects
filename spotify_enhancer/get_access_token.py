import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

# Replace with your app's credentials
client_id = "<CLIENT_ID>"
client_secret = "<CLIENT_SECRET>"
redirect_uri = "http://localhost:8080"
scope = "playlist-modify-public playlist-modify-private user-library-read"

sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)

# Get the authorization URL
auth_url = sp_oauth.get_authorize_url()
print(f"Please visit this URL to authorize the application: {auth_url}")

# Wait for the user to authorize and paste the redirect URL
response = input("Enter the URL you were redirected to: ")

# Extract the code from the response
code = sp_oauth.parse_response_code(response)

# Get the access token and refresh token
token_info = sp_oauth.get_access_token(code)

# Save the refresh token securely (you'll need to implement secure storage)
refresh_token = token_info["refresh_token"]
print(f"Your refresh token is: {refresh_token}")
print("Please store this securely and use it in your Lambda function.")
