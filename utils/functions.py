import requests
from bs4 import BeautifulSoup
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
import streamlit as st
import pickle

def scrape_billboard_hot_100():
    response = requests.get("https://www.billboard.com/charts/hot-100/")
    soup = BeautifulSoup(response.text, "html.parser")
    
    titles = []
    artists = []
    
    chart_items = soup.find_all("li", class_="o-chart-results-list__item")
    
    for item in chart_items:
        try:
            title = item.select_one(".c-title").text.strip()
            artist = item.select_one(".c-label.a-no-trucate").text.strip()
            
            titles.append(title)
            artists.append(artist)
        except AttributeError:
            continue
    
    df = pd.DataFrame({ "title": titles, "artist": artists })

    return df

def clean_billboard_df(df):
    df_clean = df.copy()

    # Standardize text fields (strip whitespace, convert to lowercase)
    df_clean['artist'] = df_clean['artist'].str.strip().str.lower()
    df_clean['title'] = df_clean['title'].str.strip().str.lower()
    
    # Remove special characters from titles (keeping letters, numbers, and basic punctuation)
    df_clean['title'] = df_clean['title'].str.replace(r'[^\w\s\'-]', '', regex=True)
    
    # Remove single or double quotes from the start and end of 'title' and 'artist'
    pattern = r"^[\"'](.*?)[\"']$"
    df_clean['title'] = df_clean['title'].str.replace(pattern, r'\1', regex=True)
    df_clean['artist'] = df_clean['artist'].str.replace(pattern, r'\1', regex=True)

    return df_clean

def clean_million_songs_df(df):
    """
    Clean the Million Songs Dataset containing only title and artist columns by:
    1. Removing duplicates
    2. Handling missing values
    3. Standardizing text fields
    4. Removing special characters from titles
    5. Removing 'b' prefix and both types of quotes
    """
    # Create a copy to avoid modifying the original
    df_clean = df.copy()

    # Remove duplicates
    df_clean = df_clean.drop_duplicates()
    
    # Handle missing values
    df_clean = df_clean.dropna()
    
    # Standardize text fields (strip whitespace, convert to lowercase)
    df_clean['artist'] = df_clean['artist'].str.strip().str.lower()
    df_clean['title'] = df_clean['title'].str.strip().str.lower()
    
    # Remove special characters from titles (keeping letters, numbers, and basic punctuation)
    df_clean['title'] = df_clean['title'].str.replace(r'[^\w\s\'-]', '', regex=True)
    
    # Regex to remove b'...' or b"..." from title and artist and keep the content in between
    pattern = r"^b?[\"'](.*?)[\"']$"
    df_clean['title'] = df_clean['title'].str.replace(pattern, r'\1', regex=True)
    df_clean['artist'] = df_clean['artist'].str.replace(pattern, r'\1', regex=True)
    
    return df_clean

def search_track_info(input_title, input_artist):
    client_id = st.secrets["SPOTIFY_CLIENT_ID"]
    client_secret = st.secrets["SPOTIFY_CLIENT_SECRET"]

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

    response = sp.search(q=f'track:{input_title} artist:{input_artist}', type='track', limit=1)

    if response["tracks"]["total"] == 0: return None

    track = response["tracks"]["items"][0]
    track_title = track["name"]
    track_popularity = track["popularity"]

    artist = sp.artist(track["artists"][0]["id"])
    artist_name = artist["name"]
    artist_genres = artist["genres"]

    album = sp.album(response["tracks"]["items"][0]["album"]["id"])
    album_popularity = album["popularity"]

    result = {
        "title": track_title,
        "artist": artist_name,
        "popularity": track_popularity,
        "album_popularity": album_popularity,
        "genres": artist_genres
    }

    return result

def process_songs_with_spotify(input_file, output_file, batch_size=50):
    """
    Process songs in batches using Spotify API and save results
    """
    # Read the input CSV
    df = pd.read_csv(input_file)
    
    # Initialize empty list for results
    all_results = []
    
    # Process in batches
    for i in range(2750, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1} of {len(df)//batch_size + 1}")
        
        batch_results = []
        for _, row in batch.iterrows():
            title = row['title']
            artist = row['artist']
            is_hot = row['isHot']
            
            try:
                track_info = {
                    "title": title,
                    "artist": artist,
                    "isHot": is_hot
                }
                spotify_info = search_track_info(title, artist)
                track_info.update(spotify_info)
                batch_results.append(track_info)
            except Exception as e:
                print(f"Error processing {title} by {artist}: {str(e)}")
                continue
        
        # Add batch results to main list
        all_results.extend(batch_results)
        
        # Save intermediate results
        temp_df = pd.DataFrame(all_results)
        temp_df.to_csv(output_file, index=False)
        
        # Small delay to respect API rate limits
        time.sleep(30)
    
    # Final save
    final_df = pd.DataFrame(all_results)
    final_df.to_csv(output_file, index=False)
    print(f"Processing complete. Saved {len(final_df)} records to {output_file}")
    return final_df

def get_song_recommendations(song_title, artist_name, n_recommendations=5):
    """
    Get song recommendations based on input song and optional artist name
    """
    df = pd.read_csv('data/5_clustered_dataset.csv')

    # Convert inputs to lowercase for matching
    song_title = song_title.strip().lower()
    artist_name = artist_name.strip().lower()

    # Find the input song on spotify
    spotify_info = search_track_info(song_title, artist_name)
    if spotify_info is None:
        return None

    # Run KMeans clustering on the result from spotify
    kmeans = pickle.load(open('kmeans/kmeans.pkl', 'rb'))
    cluster = kmeans.predict(spotify_info[["popularity", "album_popularity"]])

    # Get songs from the same cluster
    recommendations = df[df['cluster'] == cluster]
    recommendations = recommendations.sample(min(n_recommendations, len(recommendations)))
    
    return recommendations[['title', 'artist', 'popularity', 'album_popularity']]
