from config import YEARS, SPOTIFY_CREDENTIALS, CSV_PATH, DATA_FOLDER
from etl import init_spotify_api, get_playlist_ids, extract_tracks, transform_to_dataframe, save_to_csv


def run_pipeline(debug = False):
    
    sp = init_spotify_api(SPOTIFY_CREDENTIALS)
    playlists = get_playlist_ids(sp, YEARS)
    raw_data = extract_tracks(sp, playlists)
    df = transform_to_dataframe(raw_data)
    save_to_csv(df, CSV_PATH, DATA_FOLDER)

if __name__ == "__main__":
    run_pipeline()
