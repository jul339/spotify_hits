import pytest

from unittest.mock import MagicMock
import pandas as pd
from src.etl import extract_tracks, get_playlist_ids, transform_to_dataframe, save_to_csv



@pytest.fixture
def mock_spotify_client():
    sp = MagicMock()

    # Mock search results for get_playlist_ids
    sp.search.return_value = {
        "playlists": {
            "items": [{"id": "playlist_id_2023"}]
        }
    }

    # Mock playlist_tracks
    sp.playlist_tracks.return_value = {
        "items": [{
            "track": {
                "name": "Mock Song",
                "album": {"name": "Mock Album", "release_date": "2023-01-01"},
                "popularity": 80,
                "duration_ms": 210000,
                "artists": [{"id": "artist_id"}]
            }
        }]
    }

    # Mock artist info
    sp.artist.return_value = {
        "name": "Mock Artist",
        "followers": {"total": 1000000},
        "popularity": 85,
        "genres": ["pop", "dance pop"]
    }

    return sp

####################  Playlist extraction tests  ####################
def test_get_playlist_ids(mock_spotify_client):
    years = [2023]
    result = get_playlist_ids(mock_spotify_client, years)
    assert 2023 in result
    assert result[2023] == "playlist_id_2023"



####################  Track Extraction tests  ####################

def test_extract_tracks(mock_spotify_client):
    playlist_ids = {2023: "playlist_id_2023"}
    result = extract_tracks(mock_spotify_client, playlist_ids)
    assert len(result) == 1
    assert result[0]["track_name"] == "Mock Song"
    assert result[0]["artist_name"] == "Mock Artist"
    assert result[0]["artist_genres"] == "pop, dance pop"



####################  Transformation tests  ####################
def test_transform_removes_duplicates():
    raw_data = [
        {"year": 2023, "track_name": "Track1", "artist_name": "Artist1", "album_release": "2023-01-01", "track_popularity": 90,
         "track_duration_ms": 210000, "album_name": "Album1", "artist_followers": 1000, "artist_popularity": 80, "artist_genres": "pop"},
        {"year": 2023, "track_name": "Track1", "artist_name": "Artist1", "album_release": "2023-01-01", "track_popularity": 90,
         "track_duration_ms": 210000, "album_name": "Album1", "artist_followers": 1000, "artist_popularity": 80, "artist_genres": "pop"}
    ]
    df = transform_to_dataframe(raw_data)
    assert len(df) == 1

def test_transform_to_dataframe():
    raw_data = [{
        "year": 2023,
        "track_name": "Mock Song",
        "album_name": "Mock Album",
        "album_release": "2023-01-01",
        "track_popularity": 80,
        "track_duration_ms": 210000,
        "artist_name": "Mock Artist",
        "artist_followers": 1000000,
        "artist_popularity": 85,
        "artist_genres": "pop, dance pop"
    }]
    df = transform_to_dataframe(raw_data)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df.loc[0, "track_name"] == "Mock Song"
    assert pd.api.types.is_datetime64_any_dtype(df["album_release"])


def test_track_duration_is_numeric(mock_spotify_client):
    playlist_ids = {2023: "playlist_id_2023"}
    result = extract_tracks(mock_spotify_client, playlist_ids)
    assert isinstance(result[0]["track_duration_ms"], int)



####################  Saving tests  ####################


def test_save_to_csv_creates_file(tmp_path):
    df = pd.DataFrame({"a": [1], "b": [2]})
    folder = tmp_path
    file_name = "test.csv"
    
    save_to_csv(df, file_name, str(folder))
    
    file_path = folder / file_name
    assert file_path.exists()
    loaded = pd.read_csv(file_path)
    assert "a" in loaded.columns
    assert loaded.iloc[0]["a"] == 1

def test_save_to_csv_overwrites(tmp_path):
    df1 = pd.DataFrame({"a": [1]})
    df2 = pd.DataFrame({"a": [999]})
    file_path = tmp_path / "overwrite.csv"

    # Écrire une première fois
    save_to_csv(df1, "overwrite.csv", str(tmp_path))
    # Réécrire avec autre contenu
    save_to_csv(df2, "overwrite.csv", str(tmp_path))

    df_loaded = pd.read_csv(file_path)
    assert df_loaded.iloc[0]["a"] == 999

def test_save_to_csv_raises_if_folder_missing(tmp_path):
    df = pd.DataFrame({"a": [1]})
    bad_folder = tmp_path / "nonexistent"

    with pytest.raises(IOError, match="doesn't exist"):
        save_to_csv(df, "output.csv", str(bad_folder))


# def test_save_to_csv_creates_file(tmp_path):
#     df = pd.DataFrame({"a": [1], "b": [2]})
#     output_file = tmp_path / "test.csv"
#     save_to_csv(df, csv_name=str(output_file))
#     assert output_file.exists()

# def test_save_to_csv_overwrites_existing(tmp_path):
#     df1 = pd.DataFrame({"a": [1]})
#     df2 = pd.DataFrame({"a": [2]})
#     output_file = tmp_path / "test.csv"

#     save_to_csv(df1, csv_name=str(output_file))
#     save_to_csv(df2, csv_name=str(output_file))

#     df_loaded = pd.read_csv(output_file)
#     assert df_loaded.iloc[0]["a"] == 2

# def test_save_to_csv_raises_if_folder_missing(tmp_path):
#     df = pd.DataFrame({"a": [1]})
#     bad_path = tmp_path / "nonexistent_folder" / "test.csv"

#     with pytest.raises(IOError, match="doesn't exist"):
#         save_to_csv(df, path=str(bad_path), )