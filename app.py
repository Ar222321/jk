from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sklearn.neighbors import NearestNeighbors
import numpy as np

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'  # Use your preferred database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Float)
    rating_dist_total = db.Column(db.Integer)  # Total number of ratings
    counts_of_review = db.Column(db.Integer)   # Number of reviews
    pages_number = db.Column(db.Integer)        # Number of pages

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)

# Initialize the database
@app.before_first_request
def create_tables():
    db.create_all()

# Function to train the recommendation model
def train_model():
    books = Book.query.all()
    features = np.array([[book.rating_dist_total, book.counts_of_review, book.pages_number] for book in books])
    model = NearestNeighbors(n_neighbors=5)
    model.fit(features)
    return model

# Endpoint to add a new book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Book(
        name=data['name'],
        rating=data.get('rating'),
        rating_dist_total=data.get('rating_dist_total', 0),
        counts_of_review=data.get('counts_of_review', 0),
        pages_number=data.get('pages_number', 0)
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book added", "id": new_book.id}), 201

# Endpoint to retrieve all books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{"id": book.id, "name": book.name, "rating": book.rating} for book in books])

# Endpoint to retrieve a specific book by its ID
@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify({"id": book.id, "name": book.name, "rating": book.rating})

# Endpoint to update a book's information by its ID
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()
    book = Book.query.get_or_404(id)
    book.name = data.get('name', book.name)
    book.rating = data.get('rating', book.rating)
    book.rating_dist_total = data.get('rating_dist_total', book.rating_dist_total)
    book.counts_of_review = data.get('counts_of_review', book.counts_of_review)
    book.pages_number = data.get('pages_number', book.pages_number)
    db.session.commit()
    return jsonify({"message": "Book updated"})

# Endpoint to delete a book by its ID
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"})

# Endpoint to add a review for a book
@app.route('/books/<int:id>/reviews', methods=['POST'])
def add_review(id):
    data = request.get_json()
    new_review = Review(book_id=id, content=data['content'])
    db.session.add(new_review)
    db.session.commit()
    return jsonify({"message": "Review added", "id": new_review.id}), 201

# Endpoint to retrieve all reviews for a book
@app.route('/books/<int:id>/reviews', methods=['GET'])
def get_reviews(id):
    reviews = Review.query.filter_by(book_id=id).all()
    return jsonify([{"id": review.id, "content": review.content} for review in reviews])

# Endpoint to get a summary and aggregated rating for a book
@app.route('/books/<int:id>/summary', methods=['GET'])
def get_summary(id):
    book = Book.query.get_or_404(id)
    reviews = Review.query.filter_by(book_id=id).all()
    average_rating = db.session.query(db.func.avg(Review.content)).filter_by(book_id=id).scalar()
    return jsonify({
        "id": book.id,
        "name": book.name,
        "average_rating": average_rating,
        "reviews": [{"id": review.id, "content": review.content} for review in reviews]
    })

# Endpoint to get book recommendations based on user preferences
@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    model = train_model()  # Train the model when requested
    books = Book.query.all()
    features = np.array([[book.rating_dist_total, book.counts_of_review, book.pages_number] for book in books])
    
    distances, indices = model.kneighbors(features)  # Find neighbors
    recommendations = [books[i].name for i in indices.flatten()]  # Get recommended book names
    return jsonify(recommendations)

# Endpoint to generate a summary for a given book content
@app.route('/generate-summary', methods=['POST'])
def generate_summary():
    data = request.get_json()
    # Here you could integrate an external library to summarize text
    return jsonify({"summary": "Generated summary for the book content"})

if __name__ == '__main__':
    app.run(debug=True)
