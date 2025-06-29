from config import YEARS, SPOTIFY_CREDENTIALS, CSV_PATH
from etl import init_spotify_api, get_playlist_ids, extract_tracks, transform_to_dataframe, save_to_csv

DEBUG_MODE = False

def run_pipeline():
    
    years = [2024] if DEBUG_MODE else YEARS
    sp = init_spotify_api(SPOTIFY_CREDENTIALS)
    playlists = get_playlist_ids(sp, years)
    raw_data = extract_tracks(sp, playlists, DEBUG_MODE)
    df = transform_to_dataframe(raw_data)
    save_to_csv(df, CSV_PATH)

if __name__ == "__main__":
    run_pipeline()
