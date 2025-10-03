import dotenv
import os
from requests import get, post
import json
import base64
import pandas as pd

dotenv.load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type":"client_credentials"
    }

    result = post(url, headers=headers, data=data)
    result_json = json.loads(result.content)
    token = result_json['access_token']
    return token 

def get_auth_hearder(token):
    return {"Authorization": "Bearer " + token}

def search_playlist(token, playlist_name):
    headers = get_auth_hearder(token=token)
    url = "https://api.spotify.com/v1/search"
    query = f"?q={playlist_name}&type=playlist&limit=1"
    url = url + query
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['playlists']['items']
    if len(json_result) == 0:
        print("There is no playlist with provided name.")
        return None
    return json_result[0]

def get_tracks_by_playlist(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}?market=US&fields=tracks.items(track.id)"
    headers = get_auth_hearder(token=token)
    result = get(url=url, headers=headers)
    json_result = json.loads(result.content)
    return json_result['tracks']['items']

def get_track_details_by_ids(token, track_ids):
    url = f"https://api.spotify.com/v1/tracks?market=US&ids={track_ids}"
    headers = get_auth_hearder(token=token)
    result = get(url=url, headers=headers)
    json_result = json.loads(result.content)
    return json_result['tracks']
    
track_id_lists = []
track_details_dict = {
    "track_name": [],
    "artist_name": [],
    "album_name": [],
    "popularity": []
}
token = get_token()

playlist = search_playlist(token, "best songs 2023")
playlist_id = playlist['id']

tracks_result = get_tracks_by_playlist(token=token, playlist_id=playlist_id)

for track in tracks_result:
    track_id_lists.append(track['track']['id'])

track_ids = ",".join(track_id_lists)

track_details = get_track_details_by_ids(token=token, track_ids=track_ids)


for track in track_details:
    track_details_dict["track_name"].append(track['name'])
    track_details_dict["artist_name"].append(track['artists'][0]['name'])
    track_details_dict["album_name"].append(track['album']['name'])
    track_details_dict["popularity"].append(track['popularity'])

df = pd.DataFrame(track_details_dict)
df.to_csv("datasets/extracted_track_data.csv", index=False)