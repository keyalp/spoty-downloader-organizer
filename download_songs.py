import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import subprocess
from tqdm import tqdm

class DownloadSongs:
    def __init__(self, year,user):
        # Constants:
        self.user = user
        self.year = year
        self.core_numbers = '8'
        #download_directory = 'download'
        self.download_directory = f"D:\Documents\OneDrive - alu-etsetb.upc.edu\Música\SpotyDownloader\{self.year}"
        # client_credentials_manager = SpotifyClientCredentials()
        # self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        scope = "playlist-modify-public playlist-modify-private playlist-read-private"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    def start(self):
        playlists = self.sp.user_playlists(self.user,limit=50,offset=0)

        playlist_urls = [] # List with playlist URIs to download

        while playlists:
            for i, playlist in enumerate(playlists['items']):
                if playlist['tracks']['total']>0:
                    if playlist['name'].startswith(f'#{self.year}'):
                        print(
                            "%s %s" %
                            (
                            playlist['uri'],
                            playlist['name']))
                        playlist_urls.append(f"playlist/{playlist['uri'].split(':')[2]}")

            if playlists['next']:
                playlists = self.sp.next(playlists)
            else:
                playlists = None   

        for url in tqdm(playlist_urls):
            subprocess.run(['spotify_dl', '-l', url, '-mc', self.core_numbers, '-w','-o',self.download_directory])

        