from config import YEARS, SPOTIFY_CREDENTIALS, CSV_PATH
from etl import init_spotify_api, get_playlist_ids, extract_tracks, transform_to_dataframe, save_to_csv

DEBUG_MODE = True

def run_pipeline():
    
    years = [2024] if DEBUG_MODE else YEARS
    sp = init_spotify_api(SPOTIFY_CREDENTIALS)
    playlists = get_playlist_ids(sp, years)
    raw_data = extract_tracks(sp, playlists, DEBUG_MODE)
    df = transform_to_dataframe(raw_data)
    csv_path = CSV_PATH if not DEBUG_MODE else f"data/top_hits_debug.csv"
    save_to_csv(df, csv_path)

if __name__ == "__main__":
    run_pipeline()
