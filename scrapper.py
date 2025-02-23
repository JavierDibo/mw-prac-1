import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv
import time
import os
import logging
import configparser

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration from config.ini
config = configparser.ConfigParser()

# check if config.ini exists, else raise exception with message
if not os.path.exists('config.ini'):
    raise Exception("\"config.ini\n file not found. Please change the name of \"config_template.ini\" file to "
                    "\"config.ini\n after adding you public and secret spotify web API id.")

config.read('config.ini')

# Get spotify configuration parameters

# client_id = config['spotify-uja']['client_id']
# client_secret = config['spotify-uja']['client_secret']
client_id = config['spotify-personal']['client_id']
client_secret = config['spotify-personal']['client_secret']
starting_artist = config['settings']['starting_artist']  # Get starting artist parameter
c_limit = int(config['settings']['limit'])  # Get limit parameter
c_times_per_second = float(config['settings']['times_per_second'])  # Get delay parameter
c_delay = float(1 / c_times_per_second)  # Calculate delay based on times per second

# Get depth as an integer
depth = int(config['settings']['depth'])

#  Authenticate the client with your credentials
credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
spoti = spotipy.Spotify(client_credentials_manager=credentials)

# Set to track existing edges
existing_edges = set()


def safe_api_call(func, *args, retries=3, delay=c_delay, **kwargs):
    """
    Wrapper function to handle Spotify API calls with rate limiting and error handling.
    """
    for i in range(retries):
        try:
            logging.info(f"Waiting {delay} seconds before API call...")
            time.sleep(delay)
            return func(*args, **kwargs)
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 429:
                logging.warning(f"Rate limit exceeded, retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logging.error(f"API call failed: {e}")
                raise  # Re-raise other exceptions
        except Exception as e:
            logging.error(f"Unexpected error during API call: {e}")
            raise

    logging.error("Max retries exceeded for API call.")
    raise Exception("Max retries exceeded.")


def get_artist_data(artist_id, depth, current_depth=0, visited_artists=set()):
    """
    Recursively fetches artist data and collaborations up to a specified depth.

    Args:
        artist_id (str): The Spotify ID of the artist to start with.
        depth (int): The maximum depth of recursion.
        current_depth (int): The current depth of recursion (default: 0).
        visited_artists (set): A set to keep track of visited artist IDs (default: set()).
    """
    logging.info(f"Processing artist ID: {artist_id} at depth: {current_depth}")

    if artist_id in visited_artists:
        logging.info(f"Skipping already visited artist ID: {artist_id}")
        return

    visited_artists.add(artist_id)

    try:
        artist = safe_api_call(spoti.artist, artist_id)
        if not artist:
            logging.warning(f"No artist found with ID: {artist_id}")
            return

        artist_name = artist['name']

        artist_data = {
            'id': artist_id,
            'label': artist['name'],
            # 'followers': artist['followers']['total'],
            # 'genres': ', '.join(artist['genres']),
            # 'popularity': artist['popularity'],
            # 'image_url': artist['images'][0]['url'] if artist['images'] else None
        }

        # Write node data to CSV (append mode)
        try:
            with open('nodes.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=artist_data.keys())
                if os.stat('nodes.csv').st_size == 0:  # Check if file is empty using os.stat
                    writer.writeheader()
                writer.writerow(artist_data)
        except Exception as e:
            logging.error(f"Error writing artist data to nodes.csv: {e}")

        if current_depth >= depth:
            logging.info(f"Reached maximum depth ({depth}) for artist ID: {artist_id}")
            return

        # Get all collaborations of the artist
        album_types = ['album', 'single']
        for album_type in album_types:
            try:
                albums = safe_api_call(spoti.artist_albums, artist_id, album_type=album_type, limit=c_limit)

                # Handle album pagination
                while albums:
                    for album in albums['items']:
                        album_id = album['id']

                        tracks = safe_api_call(spoti.album_tracks, album_id, limit=c_limit)

                        # Handle track pagination
                        while tracks:
                            for track in tracks['items']:
                                # Get the artists for each track
                                for artist in track['artists']:
                                    collaborator_id = artist['id']

                                    # Add an edge between the current artist and this one
                                    if collaborator_id != artist_id:
                                        # Create a sorted tuple to represent the edge (ensures A->B and B->A are treated the same)
                                        edge_pair = tuple(sorted([artist_id, collaborator_id]))

                                        # Only process this edge if we haven't seen it before
                                        if edge_pair not in existing_edges:
                                            existing_edges.add(edge_pair)

                                            edge = {
                                                'source': artist_id,
                                                'target': collaborator_id
                                            }
                                            try:
                                                with open('edges.csv', 'a', newline='', encoding='utf-8') as file:
                                                    writer = csv.DictWriter(file, fieldnames=edge.keys())
                                                    if os.stat('edges.csv').st_size == 0:
                                                        writer.writeheader()
                                                    writer.writerow(edge)
                                            except Exception as e:
                                                logging.error(f"Error writing edge data to edges.csv: {e}")

                                            # Recursive call to process the collaborator, increasing the depth
                                            get_artist_data(collaborator_id, depth, current_depth + 1, visited_artists)
                                        else:
                                            logging.info(f"Skipping duplicate edge: {artist_id} - {collaborator_id}")

                            # Go to next page of tracks
                            if tracks['next']:
                                tracks = safe_api_call(spoti.next, tracks)
                            else:
                                tracks = None

                    # Go to next page of albums
                    if albums['next']:
                        albums = safe_api_call(spoti.next, albums)
                    else:
                        albums = None
            except Exception as e:
                logging.error(f"Error processing albums for {artist_name} (ID: {artist_id}) and type {album_type}: {e}")
                continue
    except Exception as e:
        logging.error(f"Error getting artist data: {e}")


# Initialize CSV files with headers
try:
    with open('nodes.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'label'])  # Adjusted to match the actual columns being written

    with open('edges.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['source', 'target'])
except Exception as e:
    logging.error(f"Error initializing CSV files: {e}")
    exit()


def clean_data(nodes_file='nodes.csv', edges_file='edges.csv'):
    """
    Cleans the nodes and edges CSV files based on identified data quality issues.
    """

    cleaned_nodes = []
    node_ids = set()  # To track unique node IDs
    node_id_counts = {}  # Track counts of each node ID
    with open(nodes_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            # Skip if any required fields are missing or empty, remove incomplete data.
            if not all([row['id'], row['label']]):
                print(f"Skipping row with missing id or label: {row}")
                continue
            if row['id'] in node_ids:
                print(f"Skipping duplicate node ID: {row['id']}")
                continue
            node_ids.add(row['id'])

            # Remove any rows with Maka and Nano Cortes Combined
            if row['label'] == 'Maka, Nano Cortés':
                print(f"Skipping merged label: {row}")
                continue

            cleaned_nodes.append(row)

            # Increment ID counts for multiple nodes
            if row['id'] not in node_id_counts:
                node_id_counts[row['id']] = 0
            node_id_counts[row['id']] += 1

    # Remove the last node with the duplicated ID if it exists
    for id, count in node_id_counts.items():
        if count > 1:
            for i in range(len(cleaned_nodes) - 1, 0, -1):
                if cleaned_nodes[i]['id'] == id:
                    cleaned_nodes.pop(i)
                    print(f"Skipping duplicated ID {id}")
                    break

    cleaned_edges = []
    with open(edges_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            # Verify that source and target exists on the cleaned_nodes
            if not (row['source'] in node_ids and row['target'] in node_ids):
                print(f"Skipping edges with missing source or target ids.")
                continue

            cleaned_edges.append(row)

    # Remove any duplicate connections between nodes
    cleaned_edges_no_dupes = []
    edges = set()
    for edge in cleaned_edges:
        edge_tuple = (edge['source'], edge['target'])
        if edge_tuple not in edges:
            cleaned_edges_no_dupes.append(edge)
            edges.add(edge_tuple)
        else:
            print(f"Skipping duplicate edge: {edge}")

    # Write cleaned data to new files
    with open('cleaned_nodes.csv', 'w', newline='', encoding='utf-8') as outfile:
        fieldnames = cleaned_nodes[0].keys() if cleaned_nodes else []
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_nodes)

    with open('cleaned_edges.csv', 'w', newline='', encoding='utf-8') as outfile:
        fieldnames = cleaned_edges_no_dupes[0].keys() if cleaned_edges_no_dupes else []
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_edges_no_dupes)

    print("Data cleaning complete. Cleaned data written to cleaned_nodes.csv and cleaned_edges.csv")


# Main execution block
if __name__ == "__main__":
    # load the artist name parameter from the configuration file
    artist_name = starting_artist

    try:
        result = safe_api_call(spoti.search, q='artist:' + artist_name, type='artist')
        items = result['artists']['items']
        if not items:
            logging.warning(f"No artists found matching: {artist_name}")
            exit()
        artist = items[0]
        artist_id = artist['id']
    except Exception as e:
        logging.error(f"Error during initial artist search: {e}")
        exit()

    # Start the search process, load depth from the config file
    visited_artists = set()
    get_artist_data(artist_id, depth=depth, visited_artists=visited_artists)

    print(f'DONE. Visited artists: {len(visited_artists)}, Unique edges: {len(existing_edges)}')
    clean_data()
