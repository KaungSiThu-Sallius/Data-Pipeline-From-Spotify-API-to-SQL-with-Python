import dotenv
import os
from requests import get, post
import json
import base64
import pandas as pd
import numpy as np
import sqlite3

dotenv.load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    """
    Fetches an access token from the Spotify API.

    Uses the client ID and secret to authenticate and retrieve a temporary
    access token for making authorized API requests.

    Returns:
        str: The access token for authenticating API requests. Returns None if the request fails.
    """
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
    """
    Search given playlist name on Spotify API.

    Args:
        playlist_name (str): The name of the playlist to be searched
        token (str): The access token for authenticating API requests.

    Returns:
        str: The unique ID of the playlist. Returns None if not found.
    """
    headers = get_auth_hearder(token=token)
    url = "https://api.spotify.com/v1/search"
    query = f"?q={playlist_name}&type=playlist&limit=1"
    url = url + query
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['playlists']['items']
    if len(json_result) == 0:
        print("There is no playlist with provided name.")
        return None
    return json_result[0]['id']

def get_tracks_by_playlist(token, playlist_id):
    """
    Retrieve tracks by playlist_id on Spotify API.

    Args:
        token (str): The access token for authenticating API requests.
        playlist_id (str): The unique ID of the playlist to retrieve tracks

    Returns:
        list: A list of dictionaries, where each dict contains a track's ID.
    """
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}?market=US&fields=tracks.items(track.id)"
    headers = get_auth_hearder(token=token)
    result = get(url=url, headers=headers)
    json_result = json.loads(result.content)
    return json_result['tracks']['items']

def get_track_details_by_ids(token, track_ids):
    """
    Retrieve tracks details by a list of track_ids on Spotify API.

    Args:
        token (str): The access token for authenticating API requests.
        track_ids (str): The id of the tracks to retrieve each track details

    Returns:
        list: The list tracks details
    """
    url = f"https://api.spotify.com/v1/tracks?market=US&ids={track_ids}"
    headers = get_auth_hearder(token=token)
    result = get(url=url, headers=headers)
    json_result = json.loads(result.content)
    return json_result['tracks']

def fetch_data_from_api(playlist_name: str) -> pd.DataFrame:
    """
    Fetching the details of the track fromm API

    Args:
        playlist_name (str): The name of the playlist to be searched    

    Returns:
        pd.DataFrame: A DataFrame containing track details.
    """
    track_id_lists = []
    track_details_dict = {
        "track_name": [],
        "artist_name": [],
        "album_name": [],
        "popularity": []
    }
    token = get_token()

    playlist_id = search_playlist(token, playlist_name)

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

    return pd.DataFrame(track_details_dict)

def clean_and_transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the data, validate the data, and transform data.

    Args:
        df: (pd.DataFrame): A DataFrame containing track details.

    Returns:
        pd.DataFrame: A cleaned and transformed DataFrame containing track details.
    """
    df = df.drop_duplicates()
    df['popularity'] = df['popularity'].astype('int')

    conditions = [
    df['popularity'] >= 80, 
    df['popularity'] >= 60
    ]
    rank = ['hits', 'popular']
    df['popularity_tier'] = np.select(conditions, rank, 'unpopular')
    return df

def load_data_to_sqlite(db_name: str, table_name: str, data: pd.DataFrame):
    """
    Load the dataframe into SQL table

    Args:
        db_name: (str): The name of the database
        table_name (str): The name of the database table
        data: (pd.DataFrame): A DataFrame containing track details.

    Returns:
        None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        data.to_sql(table_name, conn, if_exists='replace', index=False)
        print("Data loaded successfully.")
    except sqlite3.Error as e:
         print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    PLAYLIST_NAME = 'best songs 2023'
    DB_NAME = 'spotify_playlist_track.db'
    TABLE_NAME = 'spotify_playlists'
    print("--- Starting Spotify Data Pipeline ---")
    raw_df = fetch_data_from_api(PLAYLIST_NAME)

    if raw_df is not None and not raw_df.empty:
        cleaned_df = clean_and_transform_data(raw_df)

        load_data_to_sqlite(DB_NAME, TABLE_NAME, raw_df)

        print("--- Pipeline executed successfully! ---")
    else:
        print("--- Pipeline failed: Could not fetch data. ---")

