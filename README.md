# 🎵 Harmony Hub: Your Personal Music Discovery Assistant

![Harmony Hub Demo](path/to/your/demo.gif)

## 🎯 Project Summary

Harmony Hub is an intelligent music recommendation system that combines the power of Spotify's API with machine learning to help users discover new music they'll love. By analyzing song features like popularity, acoustics, and genre, our app uses K-means clustering to suggest similar tracks based on user input. The app processes data from multiple sources, including Billboard Hot 100 and the Million Song Dataset, enriched with Spotify's detailed audio features to provide accurate, personalized recommendations.

## 🌐 Try It Out!

[Launch Harmony Hub](your-deployed-app-link)

## 📊 Data Sources & Resources

- [Spotify Web API](https://developer.spotify.com/documentation/web-api/) - Used for retrieving detailed song features and metadata
- [Million Song Dataset (Subset)](http://millionsongdataset.com/) - Provides historical song data
- [Billboard Hot 100](https://www.billboard.com/charts/hot-100/) - Current popular music trends

## 🤖 Model & Evaluation

We implemented K-means clustering to group songs based on their audio features and popularity metrics. The optimal number of clusters was determined using:

- Silhouette Analysis
- Elbow Method

Our final model uses 3 clusters, which provided the best balance between cluster cohesion and separation.

## 📁 Repository Structure
