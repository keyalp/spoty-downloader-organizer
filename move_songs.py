import spotipy
from spotipy.oauth2 import SpotifyOAuth
# Given prefix and list of categories

class MoveManager:
    def __init__(self,categories, origin, dest):

        # Create the Python list dynamically
        self.source_list_playlist_name = [f'{origin} {category}' for category in categories]
        self.destination_list_playlist_name = [f'{dest} {category}' for category in categories]

        # Authenticate with Spotify API
        scope = "playlist-modify-public playlist-modify-private playlist-read-private"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    
    def get_playlist_id_by_name(self, playlist_name):
        playlists = self.sp.current_user_playlists()
 
        while playlists:
            for i, playlist in enumerate(playlists['items']):
                if playlist['name'] == playlist_name:
                    return playlist['id']
                    
            if playlists['next']:
                playlists = self.sp.next(playlists)
            else:
                playlists = None   

        return None

    def move_songs(self,source_playlist_name, destination_playlist_name,remove_source_tracks):
        # Get playlist IDs
        source_playlist_id = self.get_playlist_id_by_name(source_playlist_name)
        destination_playlist_id = self.get_playlist_id_by_name(destination_playlist_name)

        if source_playlist_id is None:
            print(f"Playlist '{source_playlist_name}' not found.")
            return
        if destination_playlist_id is None:
            print(f"Playlist '{destination_playlist_name}' not found.")
            return

        # Get tracks from source playlist
        source_tracks = self.sp.playlist_tracks(source_playlist_id)

        # Extract track URIs
        track_uris = [track['track']['uri'] for track in source_tracks['items']]
        # Check if tracks already exist in destination playlist
        destination_tracks = self.sp.playlist_tracks(destination_playlist_id)['items']
        destination_track_uris = [track['track']['uri'] for track in destination_tracks]
       
        # Add tracks to destination playlist
        if track_uris:
            tracks_to_add = list(set(track_uris) - set(destination_track_uris))
            if len(tracks_to_add)>0:
                self.sp.playlist_add_items(destination_playlist_id, tracks_to_add)

            # Remove tracks from source playlist
            if remove_source_tracks:
                print("Removing Source Tracks...")
                self.sp.playlist_remove_all_occurrences_of_items(source_playlist_id, track_uris)

    def start(self,remove_source_tracks=False):
        for source_playlist,dest_playlist in zip(self.source_list_playlist_name, self.destination_list_playlist_name):
            print(f'Moving from {source_playlist} to {dest_playlist}')
            self.move_songs(source_playlist, dest_playlist,remove_source_tracks)
