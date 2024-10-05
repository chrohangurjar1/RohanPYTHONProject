import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load Dataset (e.g., MovieLens)
data = pd.read_csv('movies_rating.csv')

# Check the DataFrame structure
print(data.columns)  # Check column names
print(data.head())   # Display first few rows of data

# Remove leading/trailing spaces from column names if necessary
data.columns = data.columns.str.strip()

# Prepare User-Item Matrix
user_item_matrix = data.pivot_table(index='Movie_ID', columns='Title', values='Rating').fillna(0)

# Split train/test sets
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Calculate Similarities using Cosine Similarity
user_similarity = cosine_similarity(user_item_matrix)
item_similarity = cosine_similarity(user_item_matrix.T)

# Recommend Movies
def recommend(user_id, user_similarity, user_item_matrix, n_recommendations=5):
    user_ratings = user_item_matrix.loc[user_id].values.reshape(1, -1)
    similarity_score = user_similarity[user_id - 1].reshape(1, -1)
    weighted_scores = similarity_score.dot(user_item_matrix)
    predicted_ratings = weighted_scores / np.abs(similarity_score).sum(axis=1, keepdims=True)
    recommendations = np.argsort(predicted_ratings[0])[::-1]
    return recommendations[:n_recommendations]

# Example user ID
user_id = 1
recommended_movies_indices = recommend(user_id, user_similarity, user_item_matrix)
recommended_movies = user_item_matrix.columns[recommended_movies_indices]
print(f"Recommended movies for User {user_id}: {list(recommended_movies)}")
