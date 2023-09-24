# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class ScrapysongsPipeline:
    def open_spider(self, spider):
        self.list_of_songs = []
        self.songs_occurrences = {}

    def process_item(self, item, spider):
        if 'band' in item:
            self.playlist_name = item['band']

        if 'song' in item:
            is_song_on_list = False
            title = item['song']
            if self.songs_occurrences == {}:
                self.songs_occurrences[title] = 1
            else:
                for song in list(self.songs_occurrences.keys()):
                    if title == song:
                        self.songs_occurrences[song] += 1
                        is_song_on_list = True
                        break
                if is_song_on_list == False:
                    self.songs_occurrences[title] = 1
        
        return item

    def close_spider(self, spider):
        scope = 'playlist-modify-public' 
        username = YOUR_SPOTIFY_ID
        token = SpotifyOAuth(scope=scope, username=username)
        spotifyObject = spotipy.Spotify(auth_manager=token)

        sorted_songs = dict(sorted(self.songs_occurrences.items(), key=lambda item: item[1], reverse=True))
        for title in sorted_songs.keys():
            result = spotifyObject.search(q="artist:" + self.playlist_name + " track:" + title, type="track")
            if result['tracks']['items'] == []:
                pass
            else:
                self.list_of_songs.append(result['tracks']['items'][0]['uri'])

        spotifyObject.user_playlist_create(user=username, name=self.playlist_name, public=True, description=None)
        prePlaylist = spotifyObject.user_playlists(user=username)
        playlist = prePlaylist['items'][0]['id']
        spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist, tracks=self.list_of_songs)




