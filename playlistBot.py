import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime, timedelta

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

    for playlist_id in playlist_ids:
        results = sp.playlist_items(playlist_id)
        for item in results['items']:
            added_at = datetime.strptime(item['added_at'], '%Y-%m-%dT%H:%M:%SZ')
            if added_at > cutoff_date:
                track = item['track']
                recent_songs.append(track['uri'])
    
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

    # Example usage


def main():

    ### ADD PLAYLIST IDS HERE
    
    playlist_ids = ['0ZQcCFqc1ziBiC1fvrrbsT','5K90H2n44UPY72YFCoHIIA','7f9o34JAe8ZSRq4GX7f0Ol','5WOVw2iX7HuDug1MfvuGA2','5X8lN5fZSrLnXzFtDEUwb9',
                    '74eAKWQUStNJFDbBUgNSFt','6gsuuOM6lSq6JnDLHO20hl','1zntMIkr4sykbGdtTQDuZp'] 
    target_playlist_id = "7bPfPkZSGbVAW1zmDfMMk4"  
    user_id = sp.current_user()['id']
    
    # Get recent songs added in the last 7 days
    recent_songs = get_recent_songs_from_playlists(sp, playlist_ids)

    # Update the existing playlist with the recent songs
    update_existing_playlist(sp, target_playlist_id, recent_songs)


# if __name__ == "__main__":
#     main()

main()
