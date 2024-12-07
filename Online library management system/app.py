from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'


# MySQL Database Connection
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='anmol@123',
        database='library_db'
    )
    return connection


# Home Route
@app.route('/')
def index():
    return render_template('index.html')


# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials"

    return render_template('login.html')


# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()

        return redirect(url_for('login'))

    return render_template('signup.html')


# Dashboard Route (User Profile)
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM borrowed_books WHERE user_id=%s AND return_date IS NULL", (user_id,))
    borrowed_books = cursor.fetchall()

    return render_template('dashboard.html', borrowed_books=borrowed_books)


# Search Books Route
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['search_query']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE title LIKE %s OR author LIKE %s OR genre LIKE %s",
                       ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))
        books = cursor.fetchall()
        return render_template('search.html', books=books)
    return render_template('search.html')


# Borrow Book Route
@app.route('/borrow/<int:book_id>')
def borrow(book_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    borrow_date = datetime.now().date()
    due_date = borrow_date + timedelta(days=14)

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the book is available (check the 'availability' column)
    cursor.execute("SELECT availability FROM books WHERE id=%s", (book_id,))
    available = cursor.fetchone()

    if available and available[0] > 0:  # Check if book is available
        cursor.execute("INSERT INTO borrowed_books (user_id, book_id, borrow_date, due_date) VALUES (%s, %s, %s, %s)",
                       (user_id, book_id, borrow_date, due_date))
        cursor.execute("UPDATE books SET availability = availability - 1 WHERE id = %s", (book_id,))
        conn.commit()
        return redirect(url_for('dashboard'))
    else:
        return "Book is not available for borrowing"


# Return Book Route
@app.route('/return/<int:borrow_id>')
def return_book(borrow_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Mark the book as returned
    cursor.execute("UPDATE borrowed_books SET return_date = %s WHERE id = %s AND user_id = %s",  # Updated 'borrow_id' to 'id'
                   (datetime.now().date(), borrow_id, user_id))
    cursor.execute("SELECT book_id FROM borrowed_books WHERE id = %s", (borrow_id,))
    book_id = cursor.fetchone()[0]
    cursor.execute("UPDATE books SET availability = availability + 1 WHERE id = %s", (book_id,))  # Use 'id' in place of 'book_id'
    conn.commit()

    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
