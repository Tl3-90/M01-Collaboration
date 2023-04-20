from flask import Flask, jsonify, request

app = Flask(__name__)

# Define some initial data for testing purposes
books = [
    {"id": 1, "book_name": "The Hitchhiker's Guide to the Galaxy", "author": "Douglas Adams", "publisher": "Pan Books"},
    {"id": 2, "book_name": "Pride and Prejudice", "author": "Jane Austen", "publisher": "T. Egerton, Whitehall"},
    {"id": 3, "book_name": "To Kill a Mockingbird", "author": "Harper Lee", "publisher": "J. B. Lippincott & Co."}
]

# Define the routes for the CRUD API

# Get all books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)

# Get a specific book by id
@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = next((book for book in books if book['id'] == id), None)
    if book:
        return jsonify(book)
    else:
        return jsonify({"message": "Book not found"}), 404

# Create a new book
@app.route('/books', methods=['POST'])
def create_book():
    # Validate input data
    if not request.json:
        return jsonify({"message": "Missing request body"}), 400
    if not all(field in request.json for field in ('id', 'book_name', 'author', 'publisher')):
        return jsonify({"message": "Missing fields in request body"}), 400
    if any(book['id'] == request.json['id'] for book in books):
        return jsonify({"message": "Book with this ID already exists"}), 400
    # Create new book
    book = {
        "id": request.json['id'],
        "book_name": request.json['book_name'],
        "author": request.json['author'],
        "publisher": request.json['publisher']
    }
    books.append(book)
    return jsonify({"message": "Book created successfully"}), 201

# Update an existing book
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    # Validate input data
    if not request.json:
        return jsonify({"message": "Missing request body"}), 400
    if not any(field in request.json for field in ('id', 'book_name', 'author', 'publisher')):
        return jsonify({"message": "No fields to update in request body"}), 400
    # Find book by ID
    book = next((book for book in books if book['id'] == id), None)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    # Update book
    book.update(request.json)
    return jsonify({"message": "Book updated successfully"}), 200

# Delete a book by id
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    # Find book by ID
    book = next((book for book in books if book['id'] == id), None)
    if book:
        books.remove(book)
        return jsonify({"message": "Book deleted successfully"}), 200
    else:
        return jsonify({"message": "Book not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)