from etl_pipeline import clean_and_transform_data
import pandas as pd

def test_clean_and_transform_data():
    test_df = pd.DataFrame({
        "track_name": ["Rewrite The Stars", "How Far I'll Go - From 'Moana'", "Heavy", "Heavy"],
        "artist_name": ["James Arthur", "Alessia Cara", "Anne-Marie", "Anne-Marie"],
        "album_name": ["The Greatest Showman: Reimagined (Deluxe)", "How Far I'll Go (From 'Moana')", "Speak Your Mind (Deluxe)", "Speak Your Mind (Deluxe)"],
        "popularity": [72,59,44, 44]
    })
    df = clean_and_transform_data(test_df)

    result_df = df.copy()
    
    assert "popularity_tier" in result_df.columns 

    actual_value = result_df[result_df['track_name']=='Rewrite The Stars']['popularity_tier'].iloc[0]
    assert actual_value == 'popular'

    assert len(result_df) == 3
