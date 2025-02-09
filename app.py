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

# Authorization
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-top-read",
    show_dialog=True
))

if st.button("Generate Collage"):
    with st.spinner("Fetching your top tracks..."):
        start_time = time.time()
        # Fetch top 100 tracks
        top_tracks = []
        for offset in [0, 50]:
            tracks = sp.current_user_top_tracks(limit=50, time_range='long_term', offset=0)
            top_tracks.extend(tracks['items'])
            end_time = time.time()
            print(f"Fetched tracks in {end_time - start_time:.2f} seconds")

        # Get unique albums
        unique_albums = {}
        for track in top_tracks:
            album_name = track['album']['name']
            artist_name = track['album']['artists'][0]['name']
            album_image_url = track['album']['images'][0]['url']

            if album_name not in unique_albums:
                unique_albums[album_name] = {'artist': artist_name, 'image_url': album_image_url}

        # Download images
        images, colors = [], []
        for album, info in unique_albums.items():
            try:
                response = requests.get(info['image_url'])
                img = Image.open(BytesIO(response.content)).convert("RGB")
                images.append(img)

                # Calculate average color
                stat = ImageStat.Stat(img)
                avg_color = tuple(int(x) for x in stat.mean[:3])
                colors.append(avg_color)

            except Exception as e:
                st.write(f"Error downloading album cover for {album}: {e}")

        if not images:
            st.error("Failed to download images.")
            st.stop()

        # Compute average background color
        avg_bg_color = tuple(np.mean(colors, axis=0).astype(int))

        # Calculate optimal grid size
        num_images = len(images)
        grid_width = math.ceil(math.sqrt(num_images))
        grid_height = math.ceil(num_images / grid_width)

        # Image dimensions
        img_width, img_height = images[0].size
        grid_image = Image.new('RGB', (img_width * grid_width, img_height * grid_height), avg_bg_color)

        # Arrange images in the grid
        for i, img in enumerate(images):
            row, col = divmod(i, grid_width)
            grid_image.paste(img, (col * img_width, row * img_height))

        # Show collage in Streamlit
        st.image(grid_image, caption="Your Album Collage", use_column_width=True)
        
        # Save and offer download
        img_buffer = BytesIO()
        grid_image.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        st.download_button("Download Image", img_buffer, file_name="spotify_grid.png", mime="image/png")

