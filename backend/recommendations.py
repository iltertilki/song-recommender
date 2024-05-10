import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from joblib import load

# Load preprocessed song features
df = pd.read_csv('song_features.csv')
X = df.drop('song', axis=1)  # Features for the recommendation model
y = df['song']  # Song identifiers

# Load the pre-trained nearest neighbors model
model = load('nearest_neighbors_model.joblib')

def enhanced_recommend(song_indices, ratings, n_recommendations=5):
    """
    Generate enhanced song recommendations based on a list of song indices and their ratings.
    
    Args:
    song_indices (list of int): Indices of songs that have been rated by the user.
    ratings (list of int): Ratings for each song indexed correspondingly.
    n_recommendations (int): Number of recommendations to return.
    
    Returns:
    list of str: Recommended song titles.
    """
    song_scores = {}

    # Iterate over each song index and its rating
    for song_index, rating in zip(song_indices, ratings):
        # Print context for debugging
        print(f"Analyzing recommendations based on {y.iloc[song_index]} rated {rating}/5")
        
        # Get the 5 nearest neighbors for the current song
        distances, indices = model.kneighbors(X.loc[song_index:song_index])
        
        # Iterate over each neighbor
        for i, idx in enumerate(indices[0]):
            song_name = y.iloc[idx]
            # Calculate weighted score (consider using distance as a factor as well)
            if song_name not in song_scores:
                song_scores[song_name] = 0
            # Weight by rating and inverse distance
            song_scores[song_name] += (5 - distances[0][i]) * rating

    # Sort songs by their calculated scores in descending order and select the top recommendations
    recommended_songs = sorted(song_scores, key=song_scores.get, reverse=True)[:n_recommendations]

    return recommended_songs
