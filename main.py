import sys
import sys
import os
import platform
from download_songs import DownloadSongs
from create_playlists import CreatePlaylists
from move_songs import MoveManager

# Constants:
user = 'keyalp'

# Add to path ffmpeg codecs converters

os.environ['SPOTIPY_CLIENT_ID'] = 'e5e70ac7bfd94bdcb80b95a904b2a3f6'
os.environ['SPOTIPY_CLIENT_SECRET'] = 'ec9ec0e93aac4f228211495c3d68b734'
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:8888'

categories = ['Techno OldSchool','Techno','House', 'Progressive House', 'Alternative', 'Drum & Bass', 'HardTech',
              'Puta Espanya', 'Catalana', 'Dembow', 'Reggaeton', 'Urban', 'Pop', 'Organic',
              'Trance', 'Deep House','DeepInHouse', 'Elrow', 'Afro House','Random','Soul House', 'Tech House',
              'TechVersions - Disco']

ffmpeg_location = 'ffmpeg-2023-12-28/bin/'

# Add to path ffmpeg codecs converters
# Check if the operating system is Windows
if platform.system() == "Windows":
    sys.path.append(ffmpeg_location)
    os.environ['PATH'] = f"{ffmpeg_location};{os.environ['PATH']}"


#0. Create Playlists (Execute only once a year.)
# playlist_creator = CreatePlaylists("0",categories)
# playlist_creator.start()
    
#1. Download Songs
download_year = '2024'
download_manager = DownloadSongs(download_year,user)
download_manager.start()

#2. Move songs to Downlaoded Folder
origin = '#2024'
dest = 'DW_2024'
move_songs = MoveManager(categories,origin,dest)
move_songs.start(remove_source_tracks=True)

