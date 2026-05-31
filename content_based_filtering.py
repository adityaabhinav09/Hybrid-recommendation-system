import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import MinMaxScaler,StandardScaler,OneHotEncoder
from category_encoders.count import CountEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, TransformerMixin
from data_cleaning import data_for_content_based_filtering
from scipy.sparse import save_npz
from sklearn.metrics.pairwise import cosine_similarity

# Cleaned data path

CLEANED_DATA_PATH = "data/cleaned_data.csv"

# Cols to transform

frequency_encode_cols = ['year']
ohe_cols = ['artist','time_signature','key']
tfidf_col = ['tags']
standard_scale_cols = ['duration_ms','loudness','tempo']
min_max_scale_cols = ['danceability','energy','speechiness','acousticness','instrumentalness','liveness','valence']

# Custom wrapper for TfidfVectorizer to work with ColumnTransformer
class TfidfVectorizerTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, max_features=85):
        self.max_features = max_features
        self.vectorizer = TfidfVectorizer(max_features=max_features)
    
    def fit(self, X, y=None):
        # Convert to 1D array if needed
        if isinstance(X, np.ndarray):
            if X.ndim == 2:
                X = X.ravel()
        elif hasattr(X, 'values'):  # pandas DataFrame/Series
            X = X.values.ravel()
        
        # Replace NaN/None values with empty strings
        X = pd.Series(X).fillna('').values
        
        self.vectorizer.fit(X)
        return self
    
    def transform(self, X):
        # Convert to 1D array if needed
        if isinstance(X, np.ndarray):
            if X.ndim == 2:
                X = X.ravel()
        elif hasattr(X, 'values'):  # pandas DataFrame/Series
            X = X.values.ravel()
        
        # Replace NaN/None values with empty strings
        X = pd.Series(X).fillna('').values
        
        return self.vectorizer.transform(X).toarray()


def train_transformer(data):
    """
    Train a column transformer on the cleaned data and save it as transformer.joblib
    
    Parameters:
    -----------
    data_path : str
        Path to the cleaned data CSV file (default: CLEANED_DATA_PATH)
    
    Returns:
    --------
    transformer : ColumnTransformer
        Fitted column transformer
    """
    
    # Create the column transformer
    transformer = ColumnTransformer(transformers=[
        ("frequency_encode", CountEncoder(normalize=True, return_df=True), frequency_encode_cols),
        ("ohe", OneHotEncoder(handle_unknown="ignore"), ohe_cols),
        ("tfidf", TfidfVectorizerTransformer(max_features=85), tfidf_col),
        ("standard_scale", StandardScaler(), standard_scale_cols),
        ("min_max_scale", MinMaxScaler(), min_max_scale_cols)
    ], remainder="passthrough", n_jobs=-1, force_int_remainder_cols=False)
    
    # Fit the transformer on the data
    transformer.fit(data)
    
    # Save the transformer as joblib file
    joblib.dump(transformer, 'transformer.joblib')
    print("Transformer trained and saved as 'transformer.joblib'")
    
def data_transform(data):
    """
    Tranform the input data using a pre-trained transformer.
    Args:
        data(array-like): The data to be transformed
    Returns:
        array-like: The transformed data.

    """
    #load the transformer

    transformer = joblib.load("transformer.joblib")
    transformed_data = transformer.transform(data)

    return transformed_data

def save_transformed_data(transformed_data,save_path):
    "Save the transformed data to specified path"
    
    save_npz(save_path,transformed_data)

def calculate_similarity_scores(input_vector,data):

    similarity_score = cosine_similarity(input_vector,data)

    return similarity_score

def recommend(song_name,songs_data,transformed_data,k=10):


    # convert song name to lowercase
    song_name = song_name.lower()

    # filter out the song from data
    song_row = songs_data.loc[songs_data['name']==song_name]

    # song index in full dataset
    song_index = song_row.index[0]

    # input vector generation
    input_vector = transformed_data[song_index].reshape(1,-1)

    # calculate similarity score
    sim_score = calculate_similarity_scores(input_vector=input_vector,data=transformed_data)

    # Top k songs
    top_k_song_idx = np.argsort(sim_score.ravel())[-k-1:][::-1]

    #Top k song names
    tok_k_song_name = songs_data.iloc[top_k_song_idx]
    
    # Print top k songs

    top_k_list = tok_k_song_name[['name','artist','spotify_preview_url']].reset_index(drop=True)

    return top_k_list

def test_recommendations(data_path,song_name,k=10):

    song_name = song_name.lower()

    data = pd.read_csv(data_path)

    data_for_content_filtering = data_for_content_based_filtering(data)

    train_transformer(data_for_content_filtering)

    tranformed_data = data_transform(data_for_content_filtering)

    save_transformed_data(tranformed_data,"data/transformed_data.npz")

    song_row = data.loc[data['name']==song_name]
    print(song_row)
    song_index = song_row.index[0]
    input_vector = tranformed_data[song_index].reshape(1,-1)
    similarity_score = calculate_similarity_scores(input_vector,tranformed_data)
    top_k_song_index = np.argsort(similarity_score.ravel())[-k-1:][::-1]

    top_k_song = data.iloc[top_k_song_index]

    print(top_k_song)


if __name__ == '__main__':
    test_recommendations(CLEANED_DATA_PATH,"whenever, wherever")
