import pandas as pd
from sqlalchemy import create_engine
import pandas as pd

# Load the CSV file with headers
df = pd.read_csv(r'C:\Users\PE586UG\OneDrive - EY\Documents\Gen AI\jk\book_ratings.csv')

# Display the first few rows to inspect the data
print("Original DataFrame:")
print(df.head())

# Clean the 'Name' column and any other necessary columns
df['Name'] = df['Name'].str.replace('Harry Potter', 'Harry Potter', regex=False)  # Adjust as needed

# Display the cleaned DataFrame
print("Cleaned DataFrame:")
print(df.head())

# Optionally, you can check for missing values
print("Missing values in each column:")
print(df.isnull().sum())


# Load the dataset
final_dataset = df

# Create a SQLAlchemy engine
DATABASE_URL = "postgresql://{user}:{password}@localhost:5432/book_management"
engine = create_engine(DATABASE_URL)

# Write the DataFrame to a new SQL table
final_dataset.to_sql('new_books_rating', engine, if_exists='replace', index=False)
