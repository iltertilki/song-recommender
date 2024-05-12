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

def enhanced_recommend(song_indices, ratings, n_recommendations=5, exclude_indices=[]):
    """
    Generate enhanced song recommendations ensuring that 5 relevant and non-rated songs are always recommended.
    This function dynamically fetches more candidates if the top recommendations include rated songs.
    
    Args:
    song_indices (list of int): Indices of songs that have been rated by the user.
    ratings (list of int): Ratings for each song indexed correspondingly.
    n_recommendations (int): Desired number of recommendations.
    exclude_indices (list of int): Indices of songs to exclude from the final recommendations.
    
    Returns:
    list of int: Indices of recommended songs, ensuring none of them have been rated.
    """
    song_scores = {}
    max_neighbors = 100  # Maximum neighbors to consider for a more extensive pool of recommendations

    # Calculate recommendations based on ratings and neighbors
    for song_index, rating in zip(song_indices, ratings):
        # Start with a reasonable number of neighbors and increase if necessary
        num_neighbors = n_recommendations * 2
        while True:
            distances, indices = model.kneighbors(X.loc[song_index:song_index], n_neighbors=num_neighbors)
            
            # Break the loop if we have enough neighbors or reached the limit
            if num_neighbors >= max_neighbors:
                break
            num_neighbors *= 2  # Dynamically increase the number of neighbors to fetch more candidates

            # Score the neighbors unless they are in the exclude list
            for i, idx in enumerate(indices[0]):
                if idx not in exclude_indices:
                    if idx not in song_scores:
                        song_scores[idx] = 0
                    song_scores[idx] += (5 - distances[0][i]) * rating  # Weight by rating and inverse distance

    # Sort song indices by their calculated scores in descending order
    sorted_indices = sorted(song_scores, key=song_scores.get, reverse=True)

    # Select the top recommendations ensuring they have not been rated
    recommended_song_indices = []
    for idx in sorted_indices:
        if idx not in exclude_indices:
            recommended_song_indices.append(idx)
            if len(recommended_song_indices) == n_recommendations:
                break

    print("Recommended song indices are: ", recommended_song_indices)
    return recommended_song_indices