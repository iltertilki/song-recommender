import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from joblib import dump

def preprocess_features(df):
    """
    Preprocesses the song feature data for training.
    """
    # Separate numeric and non-numeric data
    numeric_cols = df.select_dtypes(include=['number']).columns
    non_numeric_cols = df.columns.difference(numeric_cols)

    # Fill missing values with the column mean
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    # Normalize features
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    
    return df

def train_nearest_neighbors(df):
    """
    Trains the Nearest Neighbors model using the preprocessed features.
    """
    X = df.drop('song', axis=1)
    y = df['song']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    
    model = NearestNeighbors(n_neighbors=5, algorithm='ball_tree')
    model.fit(X_train)
    
    return model

def main():
    # Load data
    df = pd.read_csv('song_features.csv')

    # Preprocess features
    df = preprocess_features(df)

    # Train the model
    model = train_nearest_neighbors(df)

    # Save the model
    dump(model, 'nearest_neighbors_model.joblib')
    print("Model trained and saved successfully.")

if __name__ == '__main__':
    main()
