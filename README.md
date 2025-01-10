# 🎵 Melody Match: Your Personal Music Discovery Assistant

## 🎯 Project Summary

Melody Match is an intelligent music recommendation system that combines the power of Spotify's API with machine learning to help users discover new music they'll love. By analyzing song features like popularity, acoustics, and genre, our app uses K-means clustering to suggest similar tracks based on user input. The app processes data from multiple sources, including Billboard Hot 100 and the Million Song Dataset, enriched with Spotify's detailed audio features to provide accurate, personalized recommendations.

## 🌐 Try It Out!

[Launch Melody Match](https://melody-match.streamlit.app/)

## 📊 Data Sources & Resources

- [Billboard Hot 100](https://www.billboard.com/charts/hot-100/) - Current popular music trends
- [Million Song Dataset (Subset)](http://millionsongdataset.com/) - Provides historical song data
- [Spotify Web API](https://developer.spotify.com/documentation/web-api/) - Used for retrieving detailed song features and metadata

## 🤖 Model & Evaluation

We implemented K-means clustering to group songs based on their audio features and popularity metrics. The optimal number of clusters was determined using:

- Silhouette Analysis
- Elbow Method

Our final model uses 3 clusters, which provided the best balance between cluster cohesion and separation.

## 🚀 Running the App Locally

1. Clone the repository:

```bash
git clone https://github.com/markmorcos/ironhack-song-recommender.git
cd ironhack-song-recommender
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

3. Set up Spotify API credentials:
   - Create a [Spotify Developer Account](https://developer.spotify.com/dashboard)
   - Create a new application to get your credentials
   - Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and update with your credentials:

```toml
SPOTIFY_CLIENT_ID = "your_client_id_here"
SPOTIFY_CLIENT_SECRET = "your_client_secret_here"
```

4. Launch the app:

```bash
streamlit run app/recommender_app.py
```

## 🛠️ Technologies Used

- Python 3.x
- Streamlit
- Scikit-learn
- Spotipy (Spotify API wrapper)
- Pandas
- NumPy
- BeautifulSoup4

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Spotify Web API for providing comprehensive music data
- Million Song Dataset for the extensive music database
- Billboard Hot 100 for trending music data
- Streamlit for the amazing web app framework
