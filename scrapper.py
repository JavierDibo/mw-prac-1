import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv
import time
import requests
from requests.exceptions import ReadTimeout
import os

# Configure your Spotify API credentials
client_id = '75d26023724d4e89941085b8b3c7a078'
client_secret = '4f314f8b53ab43fab6d882b61a2eb7a6'

# Authenticate the client with your credentials
credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=credentials)

# Function to check if a file is empty
def is_file_empty(file_path):
    return not os.path.exists(file_path) or os.stat(file_path).st_size == 0

def get_artist_data(artist_name, depth, current_depth=0, visited_artists=None):
    if visited_artists is None:
        visited_artists = set()

    try:
        # Search for the artist by name
        result = sp.search(q='artist:' + artist_name, type='artist')
        items = result['artists']['items']
        if not items:
            return

        # Get the first result
        artist_info = items[0]
        artist_id = artist_info['id']
        artist_name_found = artist_info['name']

        # Skip if already processed
        if artist_id in visited_artists:
            return

        print(f'Processing: {artist_name_found}...')
        visited_artists.add(artist_id)

        # Gather artist data
        artist_data = {
            'id': artist_id,
            'label': artist_name_found,
            'followers': artist_info['followers']['total'],
            'genres': ', '.join(artist_info['genres']),
            'popularity': artist_info['popularity'],
            'image_url': artist_info['images'][0]['url'] if artist_info['images'] else None
        }

        # Append node data to CSV
        with open('nodes.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=artist_data.keys())
            if is_file_empty('nodes.csv'):
                writer.writeheader()
            writer.writerow(artist_data)
        # Stop recursion if maximum depth has been reached.
        if current_depth >= depth:
            return

        # Retrieve the artist's albums
        albums = sp.artist_albums(artist_id, album_type='album')
        for album in albums['items']:
            album_id = album['id']
            # Retrieve tracks for the album
            tracks = sp.album_tracks(album_id)['items']

            for track in tracks:
                # Process each artist in the track
                for track_artist in track['artists']:
                    # Avoid self-edges
                    if track_artist['id'] != artist_id:
                        edge = {
                            'source': artist_id,
                            'target': track_artist['id']
                        }
                        with open('edges.csv', 'a', newline='', encoding='utf-8') as file:
                            writer = csv.DictWriter(file, fieldnames=edge.keys())
                            if is_file_empty('edges.csv'):
                                writer.writeheader()
                            writer.writerow(edge)

                    # Recursive call using the track artist's name.
                    # Note: Consider modifying this to use the artist ID to ensure accuracy.
                    get_artist_data(track_artist['name'], depth, current_depth + 1, visited_artists)

                    time.sleep(0.5)  # Pause between API calls

    except ReadTimeout:
        print(f"Timeout processing {artist_name_found}. Retrying...")
        time.sleep(2)
        get_artist_data(artist_name, depth, current_depth, visited_artists)
    except requests.exceptions.RequestException as e:
        print(f"Request error processing {artist_name_found}: {e}")
        time.sleep(2)
        get_artist_data(artist_name, depth, current_depth, visited_artists)

# Start the process
artist_name = "Lola Indigo"  # Change this as needed
depth = 2  # Be cautious with API limits
visited_artist = set()
get_artist_data(artist_name, depth=depth, visited_artists=visited_artist)

print(f'Finished. Artists visited: {len(visited_artist)}')
