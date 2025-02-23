from collections import deque
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv
import time
import os
import logging
import configparser
from contextlib import contextmanager
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class SpotifyNetworkBuilder:
    def __init__(self, config_path='config.ini'):
        self.config = self._load_config(config_path)
        self.spoti = self._init_spotify()
        self.existing_edges = set()
        self.retry_queue = []
        self.nodes_file = 'nodes.csv'
        self.edges_file = 'edges.csv'

    def _load_config(self, config_path):
        if not os.path.exists(config_path):
            raise Exception(f"{config_path} file not found. Please rename config_template.ini to {config_path}")

        config = configparser.ConfigParser()
        config.read(config_path)
        return config

    def _init_spotify(self):
        client_id = self.config['spotify-personal']['client_id']
        client_secret = self.config['spotify-personal']['client_secret']
        # client_id = self.config['spotify-uja']['client_id']
        # client_secret = self.config['spotify-uja']['client_secret']
        credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        return spotipy.Spotify(client_credentials_manager=credentials)

    @contextmanager
    def _csv_writers(self):
        """Context manager for handling CSV files."""
        nodes_file = open(self.nodes_file, 'a', newline='', encoding='utf-8')
        edges_file = open(self.edges_file, 'a', newline='', encoding='utf-8')

        try:
            nodes_writer = csv.DictWriter(nodes_file, fieldnames=['id', 'label'])
            edges_writer = csv.DictWriter(edges_file, fieldnames=['source', 'target'])
            yield nodes_writer, edges_writer
        finally:
            nodes_file.close()
            edges_file.close()

    def safe_api_call(self, func, *args, retries=3, **kwargs):
        """Enhanced API call handler with exponential backoff."""
        delay = float(1 / float(self.config['settings']['times_per_second']))
        for i in range(retries):
            try:
                time.sleep(delay)
                return func(*args, **kwargs)
            except spotipy.exceptions.SpotifyException as e:
                if e.http_status == 429:  # Rate limit exceeded
                    delay *= 2  # Exponential backoff
                    logging.warning(f"Rate limit exceeded, retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    raise
        raise Exception("Max retries exceeded.")

    def get_artist_collaborators(self, artist_id):
        """Optimized collaborator fetching with batch processing."""
        collaborators = set()
        album_types = ['album', 'single']
        limit = int(self.config['settings']['limit'])

        for album_type in album_types:
            offset = 0
            while True:
                try:
                    albums = self.safe_api_call(
                        self.spoti.artist_albums,
                        artist_id,
                        album_type=album_type,
                        limit=limit,
                        offset=offset
                    )

                    if not albums['items']:
                        break

                    # Batch process album tracks
                    album_ids = [album['id'] for album in albums['items']]
                    for i in range(0, len(album_ids), 20):  # Spotify allows up to 20 albums per request
                        batch = album_ids[i:i + 20]
                        tracks_data = self.safe_api_call(self.spoti.albums_tracks, batch)

                        for album_tracks in tracks_data.values():
                            for track in album_tracks:
                                collaborators.update(
                                    artist['id'] for artist in track['artists']
                                    if artist['id'] != artist_id
                                )

                    offset += limit
                    if offset >= albums['total']:
                        break

                except Exception as e:
                    logging.error(f"Error fetching collaborators for {artist_id}: {e}")
                    self.retry_queue.append(('collaborators', artist_id))
                    break

        return collaborators

    def get_artist_data_bfs(self, artist_id, max_depth):
        """Optimized BFS traversal with progress tracking and batch processing."""
        logging.info(f"Starting BFS traversal from artist ID: {artist_id}")

        # Initialize tracking structures
        queue = deque([(artist_id, 0)])
        visited_artists = set([artist_id])
        current_depth = 0
        depth_artists = {0: [artist_id]}  # Track artists at each depth for progress

        # Initialize CSV files
        for filename in [self.nodes_file, self.edges_file]:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'label'] if filename == self.nodes_file else ['source', 'target'])

        # Process the starting artist
        with self._csv_writers() as (nodes_writer, edges_writer):
            while queue:
                batch = []
                # Process all artists at the current depth
                while queue and queue[0][1] == current_depth:
                    batch.append(queue.popleft())

                if not batch:  # Move to next depth
                    current_depth += 1
                    if current_depth > max_depth:
                        break
                    continue

                logging.info(f"Processing depth {current_depth} with {len(batch)} artists")
                depth_artists[current_depth] = []

                # Process batch of artists
                with tqdm(total=len(batch), desc=f"Depth {current_depth}") as pbar:
                    for current_artist_id, _ in batch:
                        try:
                            collaborators = self.get_artist_collaborators(current_artist_id)

                            for collaborator_id in collaborators:
                                edge_pair = tuple(sorted([current_artist_id, collaborator_id]))

                                if edge_pair not in self.existing_edges:
                                    self.existing_edges.add(edge_pair)
                                    edges_writer.writerow({
                                        'source': current_artist_id,
                                        'target': collaborator_id
                                    })

                                    if collaborator_id not in visited_artists:
                                        visited_artists.add(collaborator_id)
                                        collaborator = self.safe_api_call(self.spoti.artist, collaborator_id)

                                        if collaborator:
                                            nodes_writer.writerow({
                                                'id': collaborator_id,
                                                'label': collaborator['name']
                                            })

                                            if current_depth < max_depth:
                                                queue.append((collaborator_id, current_depth + 1))
                                                depth_artists[current_depth + 1].append(collaborator_id)

                        except Exception as e:
                            logging.error(f"Error processing artist {current_artist_id}: {e}")
                            self.retry_queue.append(('artist', current_artist_id))

                        pbar.update(1)

        # Process retry queue
        if self.retry_queue:
            logging.info(f"Processing {len(self.retry_queue)} failed requests...")
            self._process_retry_queue()

        return visited_artists

    def _process_retry_queue(self):
        """Process failed requests with increased delays."""
        with self._csv_writers() as (nodes_writer, edges_writer):
            for request_type, artist_id in tqdm(self.retry_queue, desc="Retrying failed requests"):
                try:
                    if request_type == 'artist':
                        artist = self.safe_api_call(self.spoti.artist, artist_id, retries=5)
                        if artist:
                            nodes_writer.writerow({
                                'id': artist_id,
                                'label': artist['name']
                            })
                    elif request_type == 'collaborators':
                        collaborators = self.get_artist_collaborators(artist_id)
                        for collaborator_id in collaborators:
                            edge_pair = tuple(sorted([artist_id, collaborator_id]))
                            if edge_pair not in self.existing_edges:
                                self.existing_edges.add(edge_pair)
                                edges_writer.writerow({
                                    'source': artist_id,
                                    'target': collaborator_id
                                })
                except Exception as e:
                    logging.error(f"Retry failed for {artist_id}: {e}")

    def build_network(self):
        """Main method to build the artist network."""
        artist_name = self.config['settings']['starting_artist']
        max_depth = int(self.config['settings']['depth'])

        try:
            result = self.safe_api_call(self.spoti.search, q='artist:' + artist_name, type='artist')
            artist = result['artists']['items'][0]
            visited_artists = self.get_artist_data_bfs(artist['id'], max_depth)

            print(f'Network building complete:')
            print(f'- Visited artists: {len(visited_artists)}')
            print(f'- Unique edges: {len(self.existing_edges)}')
            print(f'- Failed requests: {len(self.retry_queue)}')

            self.clean_data()

        except Exception as e:
            logging.error(f"Error building network: {e}")
            raise


if __name__ == "__main__":
    builder = SpotifyNetworkBuilder()
    builder.build_network()
