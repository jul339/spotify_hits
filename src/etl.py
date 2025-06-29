import os

import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import logging


logging.basicConfig(level=logging.INFO)



def init_spotify_api(credentials) -> spotipy.Spotify:
    """
    Initializes the Spotify API client using client credentials.

    Args:
        credentials (dict): Dictionary containing 'client_id' and 'client_secret'.

    Returns:
        spotipy.Spotify: Authenticated Spotify client object.

    Raises:
        RuntimeError: If there is an error during authentication.
    """
    
    logging.info("Initializing Spotify API client...")
    try:
        auth = SpotifyClientCredentials(**credentials)
        sp = spotipy.Spotify(auth_manager=auth)
        logging.info("Spotify API client initialized successfully.")
        return sp
    except Exception as e:
        raise RuntimeError(f"Error during Spotifu API initialisation : {e}")



def get_playlist_ids(sp, years) -> dict:
    """
    Retrieves the playlist ID for each year from the Spotify search API.

    Args:
        sp (spotipy.Spotify): Authenticated Spotify client.
        years (list[int]): List of years (e.g., [2020, 2021, 2022]).

    Returns:
        dict[int, str]: Dictionary mapping each year to a Spotify playlist ID.
    """

    playlist_ids = {}
    if not years or not isinstance(years, list):
        raise ValueError('Years should be a non-empty list of integers')
    for year in years:
        logging.info(f"Searching for playlist 'Top Hits of {year}'...")
        results = sp.search(q=f"Top Hits of {year}", type="playlist", limit=1)
        if results["playlists"]["items"]:
            playlist_ids[year] = results["playlists"]["items"][0]["id"]
        else:
            logging.warning(f"No playlist found for year {year}.")

    return playlist_ids



def extract_tracks(sp, playlist_ids, debug = False) -> list:
    """
    Extracts track and artist metadata from a list of Spotify playlists.

    Args:
        sp (spotipy.Spotify): Authenticated Spotify client.
        playlist_ids (dict[int, str]): Mapping of year to playlist ID.
        debug (bool): If True, limits the number of tracks processed for debugging purposes.

    Returns:
        list[dict]: List of dictionaries containing enriched track and artist metadata.

    Raises:
        ValueError: If playlist_ids is empty or None.
    """

    if not playlist_ids or not isinstance(playlist_ids, dict):
        raise ValueError('Playlist IDs should be a non-empty dictionary mapping years to playlist IDs')
    data = []
    logging.info("Extracting tracks from playlists")
    
    # Create a list of all the track with their metadata
    for year, playlist_id in playlist_ids.items():
        logging.info(f"Fetching tracks for playlist {year}...")
        results = sp.playlist_tracks(playlist_id)
        items = results["items"]
        if debug and len(items) > 10:
                items = items[:10]
        for item in items:
            track = item["track"]
            artist = sp.artist(track["artists"][0]["id"])
            data.append({
                "year": year,
                "track_name": track["name"],    
                "album_name": track["album"]["name"],
                "album_release": track["album"]["release_date"],
                "track_popularity": track["popularity"],
                "track_duration_ms": track["duration_ms"],
                "artist_name": artist["name"],
                "artist_followers": artist["followers"]["total"],
                "artist_popularity": artist["popularity"],
                "artist_genres": ", ".join(artist["genres"])
            })
    return data



def transform_to_dataframe(raw_data):
    """
    Transforms raw extracted data into a cleaned and typed Pandas DataFrame.

    Args:
        raw_data (list[dict]): List of raw track and artist data.

    Returns:
        pd.DataFrame: Cleaned DataFrame with converted types and duplicates removed.

    Raises:
        ValueError: If raw_data is None or empty.
    """
    if not raw_data or not isinstance(raw_data, list):
        raise ValueError('Extract tracks should be a non-empty list of dictionaries')
    
    logging.info("Transforming raw data into DataFrame")
    df = pd.DataFrame(raw_data)
    
    df.drop_duplicates(subset=["track_name", "artist_name", "year"], inplace=True)
    
    df["album_release"] = pd.to_datetime(df["album_release"], errors="coerce")
    
    return df



def save_to_csv(df, file_path):
    """
    Saves the given DataFrame as a CSV in the specified folder.

    Args:
        df (pd.DataFrame): DataFrame to save
        csv_name (str): Name of the CSV file
        folder (str): Target directory

    Raises:
        IOError: If write fails
        ValueError: If df is not a Pandas DataFrame
    """
    if not os.path.isdir("data"):
        logging.info("Creating 'data' directory")
        os.makedirs("data")

    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input data must be a Pandas DataFrame.")
    if os.path.exists(file_path):
        logging.warning(f"CSV '{file_path}' already exists. It will be overwrite.")

    try:
        df.to_csv(file_path, index=False)
        logging.info("CSV file saved successfully.")
    except Exception as e:
        raise IOError(f"Error writing CSV to '{file_path}': {e}")

