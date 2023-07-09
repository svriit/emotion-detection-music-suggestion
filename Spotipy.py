import spotipy
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time

auth_manager = SpotifyClientCredentials('YOUR_CLIENT_ID', 'YOUR_CLIENT_SECRET')
sp = spotipy.Spotify(auth_manager=auth_manager)

def getTrackIDs(user, playlist_id):
    track_ids = []
    playlist = sp.user_playlist(user, playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        track_ids.append(track['id'])
    return track_ids

def getTrackFeatures(id):
    track_info = sp.track(id)

    name = track_info['name']
    album = track_info['album']['name']
    artist = track_info['album']['artists'][0]['name']

    track_data = [name, album, artist]
    return track_data

emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
music_dist = {
    0: "0l9dAmBrUJLylii66JOsHB?si=e1d97b8404e34343",
    1: "1n6cpWo9ant4WguEo91KZh?si=617ea1c66ab6446b",
    2: "4cllEPvFdoX6NIVWPKai9I?si=dfa422af2e8448ef",
    3: "0deORnapZgrxFY4nsKr9JA?si=7a5aba992ea14c93",
    4: "4kvSlabrnfRCQWfN0MgtgA?si=b36add73b4a74b3a",
    5: "1n6cpWo9ant4WguEo91KZh?si=617ea1c66ab6446b",
    6: "37i9dQZEVXbMDoHDwVN2tF?si=c09391805b6c4651"
}

def fetch_playlist_tracks(user, playlist_id, emotion_name):
    track_ids = getTrackIDs(user, playlist_id)
    track_list = []
    for i in range(len(track_ids)):
        time.sleep(.3)
        track_data = getTrackFeatures(track_ids[i])
        track_list.append(track_data)
    df = pd.DataFrame(track_list, columns=['Name', 'Album', 'Artist'])
    df.to_csv(f'songs/{emotion_name.lower()}.csv')

# Fetch playlists and create CSV files
for emotion_index, playlist_id in music_dist.items():
    emotion_name = emotion_dict.get(emotion_index, "Unknown")
    fetch_playlist_tracks('spotify', playlist_id, emotion_name)
    print(f"CSV Generated for {emotion_name} playlist")
