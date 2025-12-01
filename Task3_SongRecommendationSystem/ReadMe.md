### Music Recommendation System

A Python-based recommendation system that suggests personalized songs using collaborative filtering and content-based filtering algorithms.
### Overview
This system recommends music based on user preferences and listening history. It supports multiple languages (Hindi, English, Marathi, Tamil, Telugu, Malayalam) and categorizes songs by mood (Romantic, Sad, Happy, Gym, Party, Motivating).

### Features

Dual recommendation algorithms (collaborative and content-based filtering)
Multi-language support across Indian and international music
Mood-based song categorization
Interactive rating system
Filter songs by language, mood, or genre

### How It Works


### Content-Based Filtering
Recommends songs similar to user's favorites by analyzing:

Language preference
Mood compatibility
Genre similarity

Collaborative Filtering
Suggests songs from users with similar taste patterns using Pearson correlation coefficient to calculate user similarity.

### Usage
Run the program and choose from:

Get personalized recommendations
Browse songs by filters
Rate songs (1-5 stars)
Exit

### Technical Details
Languages: Python 3.x
Libraries: Pandas, NumPy
Algorithms: Collaborative Filtering, Content-Based Filtering
Dataset: 30 songs, 5 user profiles with ratings