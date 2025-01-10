import sys
sys.path.append('.')

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from utils.functions import get_song_recommendations

def main():
    # Set page config
    st.set_page_config(
        page_title="Melody Match",
        page_icon="🎵",
        layout="centered"
    )

    # Initialize session state for navigation
    if 'page' not in st.session_state:
        st.session_state.page = 'landing'
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = None
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []

    # Navigation logic
    if st.session_state.page == 'landing':
        show_landing_page()
    elif st.session_state.page == 'selection':
        show_selection_page()
    elif st.session_state.page == 'favorites':
        show_favorites_page()

def show_landing_page():
    st.title("Melody Match")
    
    # App explanation in an expandable section
    with st.expander("App explanation"):
        st.write("""
        Welcome to the Melody Match! This app helps you discover new music based on your favorite songs.
        Simply enter a song title and optionally an artist name, and we'll recommend similar songs you might enjoy.
        """)
    
    # Input fields
    song_input = st.text_input("Type a song")
    artist_input = st.text_input("Type an artist")
    
    # Recommend button
    if st.button("Recommend!", type="primary"):
        if song_input and artist_input:
            try:
                recommendations = get_song_recommendations(song_input, artist_input)
                
                if recommendations is not None and not recommendations.empty:
                    st.session_state.recommendations = recommendations
                    st.session_state.page = 'selection'
                    st.rerun()
                else:
                    st.error("No recommendations found. Please try a different song.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a song title")
    
    if st.button("Favorites"):
        st.session_state.page = 'favorites'
        st.rerun()

def show_selection_page():
    st.title("Song Selection")
    
    if st.session_state.recommendations is not None:
        recommendations = st.session_state.recommendations
        
        # Display each recommendation in a card-like container
        for _, row in recommendations.iterrows():
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.subheader(row['title'])
                    st.write(f"Artist: {row['artist']}")
                    if 'year' in row:
                        st.write(f"Release year: {row['year']}")
                
                with col2:
                    if st.button("I like this one!", key=f"like_{row['title']}"):
                        st.success(f"You liked {row['title']} by {row['artist']}!")
                        st.session_state.favorites.append((row['title'], row['artist']))
                
                st.divider()
        
        # Back button
        if st.button("← Back to search"):
            st.session_state.page = 'landing'
            st.session_state.recommendations = None
            st.rerun()
    else:
        st.error("No recommendations to display")
        if st.button("Back to search"):
            st.session_state.page = 'landing'
            st.rerun()

def show_favorites_page():
    st.title("Favorites")

    if st.session_state.favorites:
        for favorite in st.session_state.favorites:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"{favorite[0]} by {favorite[1]}")
            with col2:
                if st.button("Remove", key=f"remove_{favorite[0]}"):
                    st.session_state.favorites.remove(favorite)
                    st.rerun()
    else:
        st.write("No favorites yet")
    
    if st.button("← Back to search"):
        st.session_state.page = 'landing'
        st.rerun()

if __name__ == "__main__":
    main() 