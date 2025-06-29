import os
import pandas as pd
import pytest
from unittest.mock import MagicMock
from src.etl import *

@pytest.fixture
def mock_spotify_client():
    sp = MagicMock()
    
    sp.search.return_value = {
        "playlists": {
            "items": [{"id": "playlist_id_2023"}]
        }
    }

    sp.playlist_tracks.return_value = {
        "items": [{
            "track": {
                "name": "Mock Track",
                "album": {"name": "Mock Album", "release_date": "2023-01-01"},
                "popularity": 85,
                "duration_ms": 210000,
                "artists": [{"id": "artist_id"}]
            }
        }]
    }

    sp.artist.return_value = {
        "name": "Mock Artist",
        "followers": {"total": 123456},
        "popularity": 90,
        "genres": ["pop", "electropop"]
    }

    return sp


def test_etl_pipeline_integration(tmp_path, mock_spotify_client):
    # IDs extraction 
    years = [2023]
    playlist_ids = get_playlist_ids(mock_spotify_client, years)
    assert playlist_ids == {2023: "playlist_id_2023"}

    # Tracks extraction
    raw_data = extract_tracks(mock_spotify_client, playlist_ids)
    assert len(raw_data) == 1
    assert raw_data[0]["track_name"] == "Mock Track"

    # 3. Transformation
    df = transform_to_dataframe(raw_data)
    assert not df.empty
    assert "album_release" in df.columns
    assert pd.api.types.is_datetime64_any_dtype(df["album_release"])

    # 4. Save to csv
    output_file = tmp_path / "test_output.csv"
    save_to_csv(df, csv_name=str(output_file), folder='data')
    assert output_file.exists()

    # 5. Vérification du contenu
    loaded = pd.read_csv(output_file)
    assert "track_name" in loaded.columns
    assert loaded.iloc[0]["artist_name"] == "Mock Artist"
