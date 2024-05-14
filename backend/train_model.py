import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from joblib import dump, load
import os

def preprocess_features(df, save_scaler=False):
    """
    Preprocesses the song feature data for training.
    """
    numeric_cols = df.select_dtypes(include=['number']).columns
    non_numeric_cols = df.columns.difference(numeric_cols)

    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    return df

def train_nearest_neighbors(df):
    """
    Trains the Nearest Neighbors model using the preprocessed features.
    """
    X = df.drop('song', axis=1)  # Assuming 'song' column is the identifier
    model = NearestNeighbors(n_neighbors=5, algorithm='ball_tree')
    model.fit(X)
    
    return model

def main():
    try:
        # Load data
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, 'song_features.csv')
        df = pd.read_csv(file_path)

        # Preprocess features
        df = preprocess_features(df, save_scaler=True)

        # Train the model
        model = train_nearest_neighbors(df)

        # Save the model
        dump(model, 'nearest_neighbors_model.joblib')
        print("Model trained and saved successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
