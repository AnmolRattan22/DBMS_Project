# Online Library Management System

## Features

### Front End:
- **User Login/Signup Interface**
  - Secure authentication system to allow users to create accounts and log in.
- **Search for Books**
  - Users can search for books by:
    - Title
    - Author
    - Genre
- **Borrowed Books List**
  - Display a list of books borrowed by the user.
  - Show due dates for returning borrowed books.

### Back End:
- **MySQL Database**
  - Manages:
    - User information (login credentials and profiles).
    - Book records (titles, authors, genres, and availability).
    - Borrow/return records (tracking borrowing history and due dates).

- **Flask Framework**
  - Python-based back end to handle routing, database interactions, and business logic.

## Installation Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/online-library-management-system.git
   cd online-library-management-system
   ```

2. **Set Up the Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate   # For Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**
   - Import the MySQL schema:
     ```bash
     mysql -u <username> -p < database_name> < schema.sql
     ```
   - Update the database configuration in `config.py`:
     ```python
     DATABASE_URI = "mysql+pymysql://<username>:<password>@<host>/<database_name>"
     ```

5. **Run the Application**
   ```bash
   flask run
   ```
   The application will be available at `http://127.0.0.1:5000`.

## Usage
- Open the application in your web browser.
- Sign up or log in to access the system.
- Search for books, view borrowed books, and track due dates.

## Folder Structure
```
online-library-management-system/
├── app.py              # Main application file
├── templates/          # HTML templates for the front end
├── static/             # CSS and other static files
├── models.py           # Database models
├── config.py           # Configuration file (e.g., database URI)
├── requirements.txt    # Python dependencies
├── schema.sql          # SQL schema for the database
```

## Contributing
- Contributions are welcome! Please fork the repository and submit a pull request with your changes.
- For major changes, open an issue first to discuss your ideas.
- 
## Contact
For questions or suggestions, feel free to contact [anmoldhiman2005@gmail.com] or open an issue in the repository.

