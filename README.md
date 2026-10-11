# UserManager

Current version: **v1.1**

UserManager is a simple Django application for managing user records. It was built as a personal learning project and provides a complete CRUD flow for names and ages.

## Technologies

- Python
- Django 6.1.2
- Bootstrap 5.3.2
- HTML, CSS, and JavaScript
- SQLite

## Features

- Create and validate user records
- List registered users
- Edit existing users
- Delete users with a confirmation page
- Success and error messages
- Responsive Bootstrap interface
- Dark and light themes with saved preferences
- Smooth transitions with reduced-motion support

## Running locally

1. Create a virtual environment:

   ```powershell
   python -m venv venv
   ```

2. Activate the environment on Windows:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

4. Apply the database migrations:

   ```powershell
   python manage.py migrate
   ```

5. Start the development server:

   ```powershell
   python manage.py runserver
   ```

Open `http://127.0.0.1:8000/` in your browser.
