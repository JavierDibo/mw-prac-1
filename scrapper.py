import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv
import time
import requests
from requests.exceptions import ReadTimeout
from collections import deque

# Configure your Spotify API credentials
client_id = '75d26023724d4e89941085b8b3c7a078'
client_secret = '4f314f8b53ab43fab6d882b61a2eb7a6'

# Authenticate the client with your credentials
credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=credentials)

def process_artist(artist_name, depth):
    # Initialize data structures
    visited_artists = set()
    artist_queue = deque()  # Queue of (artist_name, depth) tuples
    artist_queue.append((artist_name, 0))

    # Initialize CSV files with headers
    with open('nodes.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'label', 'followers', 'genres', 'popularity', 'image_url'], quoting=csv.QUOTE_ALL)
        writer.writeheader()

    with open('edges.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['source', 'target'])
        writer.writeheader()

    while artist_queue:
        current_artist_name, current_depth = artist_queue.popleft()
        
        try:
            # Search for artist
            result = sp.search(q='artist:' + current_artist_name, type='artist')
            items = result['artists']['items']
            if not items:
                continue

            # Get first result
            artist = items[0]
            artist_id = artist['id']
            artist_name = artist['name']

            if artist_id in visited_artists:  # Skip if already processed
                continue

            print(f'Processing: {artist_name} at depth {current_depth}...')
            visited_artists.add(artist_id)

            # Save artist data
            artist_data = {
                'id': artist_id,
                'label': artist['name'],
                'followers': artist['followers']['total'],
                'genres': ', '.join(artist['genres']),
                'popularity': artist['popularity'],
                'image_url': artist['images'][0]['url'] if artist['images'] else None
            }

            # Write node data
            with open('nodes.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=artist_data.keys(), quoting=csv.QUOTE_ALL)
                writer.writerow(artist_data)

            # If at max depth, skip getting collaborators
            if current_depth >= depth:
                continue

            # Process all albums
            albums = sp.artist_albums(artist_id, album_type='album')
            processed_collaborators = set()  # Track collaborators for this artist

            for album in albums['items']:
                # Get all tracks
                tracks = sp.album_tracks(album['id'])['items']

                for track in tracks:
                    # Process each collaborator
                    for collab_artist in track['artists']:
                        collab_id = collab_artist['id']
                        
                        # Skip if same artist or already processed this collaboration
                        if collab_id != artist_id and collab_id not in processed_collaborators:
                            processed_collaborators.add(collab_id)
                            
                            # Save edge
                            edge = {
                                'source': artist_id,
                                'target': collab_id
                            }
                            with open('edges.csv', 'a', newline='', encoding='utf-8') as file:
                                writer = csv.DictWriter(file, fieldnames=edge.keys())
                                writer.writerow(edge)
                            
                            # Add collaborator to queue for next level
                            artist_queue.append((collab_artist['name'], current_depth + 1))

                time.sleep(0.5)  # Rate limiting

        except ReadTimeout:
            print(f"Timeout processing {current_artist_name}. Retrying...")
            time.sleep(2)
            artist_queue.appendleft((current_artist_name, current_depth))  # Put back in queue to retry

        except requests.exceptions.RequestException as e:
            print(f"Request error processing {current_artist_name}: {e}")
            time.sleep(2)
            artist_queue.appendleft((current_artist_name, current_depth))  # Put back in queue to retry

    return visited_artists

# Start the search process
artist_name = "Travis Scott"  # Change this to your favorite artist
depth = 2  # Be careful with Spotify API Limits!!
visited_artists = process_artist(artist_name, depth)

print(f'DONE. Artists visited: {len(visited_artists)}')