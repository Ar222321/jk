from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Book  # Make sure your Book model is imported
from Summarizer import generate_summary  # Adjust the import based on your file structure

# Update with your actual database details
DATABASE_URL = "postgresql://{user}:{password}@localhost:5432/book_management"

# Create engine and session
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_connection():
    try:
        # Create a connection to the database
        with engine.connect() as connection:
            print("Connection to the database is successful!")
    except Exception as e:
        print(f"Error connecting to the database: {e}")

def get_book_by_id(db, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

def main(book_id: int):
    # Test the database connection
    test_connection()

    # Create a new session
    db = SessionLocal()
    try:
        # Get the book by ID
        book = get_book_by_id(db, book_id)
        if book:
            print(f"Book Title: {book.title}")
            print(f"Original Summary: {book.summary}")

            # Generate summary
            summary = generate_summary(book.summary)
            print(f"Generated Summary: {summary}")

            # Optionally, you can update the book's summary in the database
            book.summary = summary
            db.commit()
            print("Book summary updated in the database.")
        else:
            print("Book not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    book_id = int(input("Enter the book ID: "))  # Get the book ID from user input
    main(book_id)
