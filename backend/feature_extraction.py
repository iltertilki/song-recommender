import os
import librosa
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import logging

# Setup basic configuration for logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_features(file_path):
    try:
        y, sr = librosa.load(file_path)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr).mean()
        rmse = librosa.feature.rms(y=y).mean()
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr).mean()
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr).mean()
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr).mean()
        zero_crossing_rate = librosa.feature.zero_crossing_rate(y).mean()
        mfcc = librosa.feature.mfcc(y=y, sr=sr).mean(axis=1)
        features = {'tempo': tempo, 'chroma_stft': chroma_stft, 'rmse': rmse, 'spectral_centroid': spectral_centroid,
                    'spectral_bandwidth': spectral_bandwidth, 'rolloff': rolloff, 'zero_crossing_rate': zero_crossing_rate}
        for i, coef in enumerate(mfcc):
            features[f'mfcc_{i+1}'] = coef
        return features
    except Exception as e:
        logging.error(f"Failed to process {file_path}: {e}")
        return None

def process_directory(directory):
    features_list = []
    for file_name in os.listdir(directory):
        if file_name.endswith('.mp3'):
            file_path = os.path.join(directory, file_name)
            features = extract_features(file_path)
            if features is not None:  # Only append if extraction was successful
                features['song'] = file_name
                features_list.append(features)
    print(f"Completed processing directory: {directory}")
    return features_list

def main():
    root_dir = r'D:\MMC-Project\song-recommender\backend\data'
    directories = [os.path.join(root_dir, f"{i:03d}") for i in range(156) if os.path.exists(os.path.join(root_dir, f"{i:03d}"))]
    with ThreadPoolExecutor(max_workers=52) as executor:
        results = executor.map(process_directory, directories)
    all_features = [feature for result in results for feature in result if feature is not None]
    df = pd.DataFrame(all_features)
    df.to_csv('song_features.csv', index=False)
    print("All directories processed and data saved to CSV.")

if __name__ == "__main__":
    main()