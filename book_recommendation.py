import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np
import re

# Load your dataset
df = pd.read_csv("book_rating_data.csv")

# Enhanced data cleaning function
def clean_data(df):
    # Remove unwanted characters and convert to numeric
    df['RatingDistTotal'] = df['RatingDistTotal'].apply(lambda x: re.sub(r'\D', '', str(x)))  # Keep only digits
    df['RatingDistTotal'] = pd.to_numeric(df['RatingDistTotal'], errors='coerce')  # Convert to numeric

    df['CountsOfReview'] = pd.to_numeric(df['CountsOfReview'], errors='coerce')  # Convert to numeric
    df['pagesNumber'] = pd.to_numeric(df['pagesNumber'], errors='coerce')  # Convert to numeric
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')  # Convert to numeric
    
    # Drop rows with NaN values in important columns
    df = df.dropna(subset=['RatingDistTotal', 'CountsOfReview', 'pagesNumber', 'Rating'])
    return df

# Clean the DataFrame
df = clean_data(df)

# Train the Nearest Neighbors model using additional features
features = df[['RatingDistTotal', 'CountsOfReview', 'pagesNumber', 'Rating']]
model = NearestNeighbors(n_neighbors=5)
model.fit(features)

def recommend_books(book_name, model, df):
    """
    Recommend books based on the input book name.
    
    Parameters:
    - book_name: str, the name of the book for which recommendations are needed.
    - model: NearestNeighbors model, the trained model for making recommendations.
    - df: DataFrame, the dataset containing book information.
    
    Returns:
    - List of recommended book names based on the input book.
    """
    book_name_normalized = book_name.strip()
    
    if book_name_normalized in df['Name'].values:
        idx = df[df['Name'] == book_name_normalized].index[0]
        
        # Extract features for the selected book
        book_features = df[['RatingDistTotal', 'CountsOfReview', 'pagesNumber', 'Rating']].iloc[idx].values.reshape(1, -1)
        
        # Get the nearest neighbors
        distances, indices = model.kneighbors(book_features)
        
        # Get recommended book names based on the indices
        recommended_books = df['Name'].iloc[indices.flatten()].tolist()
        
        return recommended_books
    else:
        return []

# Get user input for the book name
input_book_name = input("Enter the name of the book you're interested in: ")

# Get recommendations
recommended_books = recommend_books(input_book_name, model, df)

# Output the recommended books
if recommended_books:
    print("Recommended books based on your interest:")
    for book in recommended_books:
        print(book)
else:
    print("Sorry, the book you entered is not in the dataset.")

"""
# Example usage:
# Call the function with the book name you are interested in.
input_book_name = "Bill Bryson's African Diary"  # Replace with your desired book name
recommended_books = recommend_books(input_book_name, model, df)

# Output the recommended books
print("Recommended books based on your interest:")
for book in recommended_books:
    print(book)
"""