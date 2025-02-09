import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from PIL import Image, ImageStat
from io import BytesIO
import numpy as np
import math
import streamlit as st
import time

# Streamlit UI
st.title("Spotify Album Grid Generator by Quentin Meat")
st.write("Authorize with Spotify and generate a collage of your favorite albums!")

# Spotify API credentials (replace with your own)
CLIENT_ID = "43e1119119344adcb121bc875d9d8880"
CLIENT_SECRET = "ef2007cdeda7488cbc5ffcd5c99b82dc"
REDIRECT_URI = "https://spotify-album-grid-nxymkrtq7ubmdvttd2r7fd.streamlit.app/"

# Define the scope for permissions
SCOPE = "user-top-read"

# Initialize Spotipy with OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    show_dialog=True  # Forces re-authorization on each run
))

st.title("Your 100 Favorite Tracks")

def get_top_tracks():
    tracks = []
    # Spotify API returns a maximum of 50 tracks per request, so we use two requests.
    for offset in [0, 50]:
        response = sp.current_user_top_tracks(limit=50, time_range="long_term", offset=offset)
        tracks.extend(response["items"])
    return tracks

try:
    top_tracks = get_top_tracks()
except Exception as e:
    st.error(f"Error fetching tracks: {e}")
    top_tracks = []

if top_tracks:
    for i, track in enumerate(top_tracks, start=1):
        track_name = track["name"]
        # In case there are multiple artists, join their names with a comma
        artist_names = ", ".join(artist["name"] for artist in track["artists"])
        st.write(f"{i}. {track_name} by {artist_names}")
else:
    st.write("No tracks found. Please make sure you have authorized the app and have sufficient listening history.")
