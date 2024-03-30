import spotipy
from spotipy.oauth2 import SpotifyOAuth

class CreatePlaylists:
    def __init__(self,year, categories):

        # Create the Python list dynamically
        self.playlist_list = [f'#{year} {category}' for category in categories]
        # Print the resulting Python list
        print(self.playlist_list)
        scope = "playlist-modify-public"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    def start(self):
        user_id = self.sp.me()['id']
        for playlist in self.playlist_list:
            self.sp.user_playlist_create(user_id, playlist)

