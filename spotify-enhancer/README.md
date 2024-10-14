# Spotify Enhancer

The **Spotify Enhancer** is a serverless application designed to streamline playlist management on Spotify. It leverages AWS Lambda to create, search, and modify playlists based on user-defined input, making it easier for users to curate their music experience.

## Overview


### Playlist Tracks Additioner / `post-playlist-additions`
The main feature of the Spotify Enhancer is the Playlist Additioner function that performs the following tasks:

- **Authenticate with Spotify:** It uses the OAuth 2.0 protocol to obtain an access token using a refresh token.
- **Manage Playlists:** It checks for existing playlists by name and creates a new playlist if one does not exist.
- **Add Tracks:** It searches for tracks based on the provided name and artist, retrieves their Spotify IDs, and adds them to the specified playlist.
- **Response Handling:** It returns a summary of the added tracks and any tracks that could not be found.

## Authentication Process

To authenticate with the Spotify API and obtain a refresh token, follow these steps:

1. **Set Up Spotify Developer Account:**
   - Create an app at the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
   - Obtain your **Client ID**, **Client Secret**, and set the **Redirect URI** (e.g., `http://localhost:3000`).

2. **Run the Authentication Script:**
   - Use the provided authentication script in the repository to obtain a refresh token. This script will guide you through the OAuth flow, allowing you to authorize the application and retrieve your tokens.

3. **Store the Refresh Token:**
   - After successfully running the script, store the refresh token securely. This token will be used in the Lambda function to obtain access tokens for subsequent API calls.

## Example Test Event

To test the Lambda function, you can use the following example event payload:

```
{
  "playlist_name": "Cool Cats with Sassy Swing",
  "tracks": [
    {"name": "All Blues", "artist": "Miles Davis"},
    {"name": "In a Sentimental Mood", "artist": "Duke Ellington & John Coltrane"},
    {"name": "Freddie Freeloader", "artist": "Miles Davis"}
  ]
}
```

### Suggestion: 
You can get such bodies by asking track/playlist suggestion from ChatGPT in such format.

### Remote invoke test:
```
sam remote invoke --stack-name spotify-enhancer PostPlaylistAdditionsFunction --event-file post-playlist-additions-api/events/test_event.json
```


Use https://reqbin.com/curl with this body
```
curl -X POST "https://{api_id}.execute-api.eu-west-1.amazonaws.com/v1/add-to-playlist/" \
-H "Content-Type: application/json" \
-H "x-api-key: <API_KEY_FROM_API_GW>" \
-d '{"playlist_name": "My Chill Playlist", "tracks": [{"name": "Lose Yourself", "artist": "Eminem"}, {"name": "Shape of You", "artist": "Ed Sheeran"}]}'
```