import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime, timedelta
import math

# Initialize the Spotify API client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="f6f6de34e09741d28b1766703ec2560a",
                                               client_secret="19cd0d5906204557934a27406a24e4ca",
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-library-read playlist-modify-public playlist-read-private"))

def chunk_list(lst, n):
    if n == 0:
        return [lst]  # Return the whole list as a single chunk if n is zero
    avg = len(lst) / float(n)
    out = []
    last = 0.0

    while last < len(lst):
        out.append(lst[int(last):int(last + avg)])
        last += avg
    return out

def get_recent_songs_from_playlists(sp, playlist_ids, days=6):
    recent_songs = []
    cutoff_date = datetime.now() - timedelta(days=days)
    print(f"Cutoff date: {cutoff_date}")

    for playlist_id in playlist_ids:
        offset = 0
        while True:
            results = sp.playlist_items(playlist_id, offset=offset, limit=100)
            if not results['items']:
                break
            print(f"Results for playlist {playlist_id} with offset {offset}: {len(results['items'])} items")
            for count, item in enumerate(results['items'], start=1):
                added_at = item['added_at']
                print(f"{count}: {item['track']['name']}")
                try:
                    added_at = datetime.strptime(added_at, '%Y-%m-%dT%H:%M:%SZ')
                    if added_at > cutoff_date:
                        track = item['track']
                        recent_songs.append(track['uri'])
                except ValueError as e:
                    print(f"Error parsing date at iteration {count}: {e}")
            offset += 100
    
    return recent_songs

def update_existing_playlist(sp, playlist_id, song_uris):
    # Clear the existing playlist
    sp.playlist_replace_items(playlist_id, [])
    print(f"Cleared playlist with ID: {playlist_id}")
    # Add the new songs to the playlist
    chunks = chunk_list(song_uris, math.ceil(len(song_uris)/99))
    for x in chunks:
        sp.playlist_add_items(playlist_id, x)
        print(f"Updated playlist with ID: {playlist_id} with {len(song_uris)} songs")

def update_playlist_with_recent_songs(sp, target_playlist_id, playlist_ids, days):
    # Get recent songs added in the last specified number of days
    recent_songs = get_recent_songs_from_playlists(sp, playlist_ids, days)

    # Update the existing playlist with the recent songs
    update_existing_playlist(sp, target_playlist_id, recent_songs)

def main():

    ### PUBLIC COLLECTION // GROCERIES
    # target_playlist_id = "7bPfPkZSGbVAW1zmDfMMk4"
    # playlist_ids = ['0ZQcCFqc1ziBiC1fvrrbsT', '5K90H2n44UPY72YFCoHIIA', '7f9o34JAe8ZSRq4GX7f0Ol', '5WOVw2iX7HuDug1MfvuGA2', '5X8lN5fZSrLnXzFtDEUwb9','74eAKWQUStNJFDbBUgNSFt', '6gsuuOM6lSq6JnDLHO20hl', '1zntMIkr4sykbGdtTQDuZp']
    days = 6
    # update_playlist_with_recent_songs(sp, target_playlist_id, playlist_ids, days)

    ### ALL NEW 
    allnew_target = "4dCo4dtHPiQzcGZ76k75d0"
    allnew_playlistids=['37i9dQZF1DX8C585qnMYHP']
    #allnew_playlistids=['37i9dQZF1DXdbXrPNafg9d','37i9dQZF1DX5J7FIl4q56G','37i9dQZF1DX11otjJ7crqp','37i9dQZF1DX0KpeLFwA3tO','37i9dQZF1DWZryfp6NSvtz','37i9dQZF1DWZCOSaet9tpB','37i9dQZF1DX4dyzvuaRJ0n','37i9dQZF1DWV1aMSQY91oR','37i9dQZF1DX82GYcclJ3Ug','37i9dQZF1DX4JAvHpjipBk','37i9dQZF1DWT2jS7NwYPVI','37i9dQZF1DX7oMO417tEZs','37i9dQZF1DWUzFXarNiofw','37i9dQZF1DX4SBhb3fqCJd','37i9dQZF1DWYV7OOaGhoH0']
    update_playlist_with_recent_songs(sp, allnew_target, allnew_playlistids, days)

    ### Fresh Finds
    # freshfinds_target = '6nUntr0HxRVBqyeCUrg0Ix'
    # freshfinds_playlistids = ['37i9dQZF1DWWjGdmeTyeJ6','37i9dQZF1DX6bBjHfdRnza','37i9dQZF1DX8C585qnMYHP','37i9dQZF1DXdS3lvGe1GrT','37i9dQZF1DX2wnPyeao7oY','37i9dQZF1DWW4igXXl2Qkp','37i9dQZF1DWT0upuUFtT7o','37i9dQZF1DXcWL5K0oNHcG','37i9dQZF1DXagUeYbNSnOA','37i9dQZF1DX3u9TSHqpdJC','37i9dQZF1DWUFAJPVM3HTX','37i9dQZF1DX78toxP7mOaJ']
    # update_playlist_with_recent_songs(sp, freshfinds_target, freshfinds_playlistids, days)


if __name__ == "__main__":
    main()
