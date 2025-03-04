import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials (замените на свои)
CLIENT_ID = "43e1119119344adcb121bc875d9d8880"
CLIENT_SECRET = "ef2007cdeda7488cbc5ffcd5c99b82dc"
REDIRECT_URI = "https://spotify-album-grid-nxymkrtq7ubmdvttd2r7fd.streamlit.app/"  # Если разворачиваете на Streamlit Cloud, укажите ваш URL

# Define the scope for permissions
SCOPE = "user-top-read"

# Initialize Spotipy with OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    show_dialog=True  # Заставляет запрашивать авторизацию при каждом запуске
))

st.title("Your 100 Favorite Tracks")

# Получим информацию о пользователе для проверки успешной авторизации
try:
    user_info = sp.current_user()
    st.write("User Info:", user_info)
except Exception as e:
    st.error(f"Error fetching user info: {e}")

def get_top_tracks():
    tracks = []
    for offset in [0, 50]:
        # Можно попробовать разные временные диапазоны: "long_term", "medium_term", "short_term"
        response = sp.current_user_top_tracks(limit=50, time_range="long_term", offset=offset)
        st.write(f"Response for offset {offset}:", response)  # Отладочный вывод
        # Если по каким-либо причинам в ответе отсутствует ключ "items", используем пустой список
        tracks.extend(response.get("items", []))
    return tracks

try:
    top_tracks = get_top_tracks()
except Exception as e:
    st.error(f"Error fetching tracks: {e}")
    top_tracks = []

st.write("Total tracks fetched:", len(top_tracks))

if top_tracks:
    for i, track in enumerate(top_tracks, start=1):
        track_name = track.get("name", "No name")
        artist_names = ", ".join(artist.get("name", "Unknown") for artist in track.get("artists", []))
        st.write(f"{i}. {track_name} by {artist_names}")
else:
    st.write("No tracks found. Please ensure you've authorized the app and have sufficient listening history.")
