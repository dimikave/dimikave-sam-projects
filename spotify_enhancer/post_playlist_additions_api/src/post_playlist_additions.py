import json
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def lambda_handler(event, context):
    # Set up Spotify client with refresh token
    sp_oauth = SpotifyOAuth(
        client_id=os.environ["SPOTIFY_CLIENT_ID"],
        client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
        redirect_uri=os.environ["SPOTIFY_REDIRECT_URI"],
        scope="playlist-modify-public playlist-modify-private user-library-read",
    )

    # Get a new access token using the refresh token
    token_info = sp_oauth.refresh_access_token(os.environ["SPOTIFY_REFRESH_TOKEN"])

    sp = spotipy.Spotify(auth=token_info["access_token"])

    # Parse the incoming event
    body = json.loads(event["body"])
    playlist_name = body["playlist_name"]
    tracks = body["tracks"]

    # Find the playlist or create a new one
    playlists = sp.current_user_playlists()
    playlist_id = None
    for playlist in playlists["items"]:
        if similar(playlist["name"].lower(), playlist_name.lower()) > 0.8:
            playlist_id = playlist["id"]
            playlist_name = playlist["name"]  # Use the actual playlist name
            break

    if not playlist_id:
        # Create a new playlist
        user_id = sp.me()["id"]
        new_playlist = sp.user_playlist_create(user_id, playlist_name)
        playlist_id = new_playlist["id"]

    # Search for tracks and collect their Spotify IDs
    track_ids = []
    not_found_tracks = []
    for track in tracks:
        result = sp.search(q=f"track:{track['name']} artist:{track['artist']}", type="track", limit=1)
        if result["tracks"]["items"]:
            track_ids.append(result["tracks"]["items"][0]["id"])
        else:
            not_found_tracks.append(f"{track['name']} by {track['artist']}")

    # Add tracks to the playlist
    if track_ids:
        sp.playlist_add_items(playlist_id, track_ids)

    # Prepare the response
    response = {"added_tracks": len(track_ids), "playlist_name": playlist_name, "not_found_tracks": not_found_tracks}

    if track_ids:
        return {"statusCode": 200, "body": json.dumps(response)}
    else:
        return {"statusCode": 400, "body": json.dumps(response)}
