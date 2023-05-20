from spotipy import Spotify

from top100 import top_100, year, date
import os

YEAR = year
DATE = date
ID = os.environ["Client ID"]
secret = os.environ["Client Secret"]
URI = "https://example.com"
SCOPE = "playlist-modify-private"
TRACKS = top_100()
SYMBOLS = ["X", "x", "Featuring", "(", "&", "+"]


def authorization(scope=""):
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=ID,
                                                   client_secret=secret,
                                                   redirect_uri=URI,
                                                   scope=scope,
                                                   )
                         )

    return sp


sp = authorization(scope=SCOPE)
user_id = sp.current_user()["id"]
print(user_id)


def create_uris(tracks=TRACKS):
    uris = []
    for (track, artist) in tracks.items():
        for symbol in SYMBOLS:
            artist = artist.split(symbol)[0] if symbol in artist else artist

        result = sp.search(q=f"track:{track} artist:{artist}", type="track")
        # print(result)
        try:
            uri = result["tracks"]["items"][0]["uri"]
            uris.append(uri)
        except IndexError:
            print(f"{track} {artist} is not on Spotify")

    return uris


playlist = sp.user_playlist_create(user_id,
                                   name=date + " Billboard 100",
                                   public=False,
                                   description=f"This playlist contains top 100 tracks on {date}")

playlist_id = playlist["id"]  # get the playlist id
songs = create_uris()
sp.playlist_add_items(playlist_id, songs)  # 2 args: playlist_id and lists o uris
