
About This Project

This project is a World Geography Quiz application. Unlike my previous projects such as Submit Search, Wiki Commerce, and Mail Network, this project focuses on interactive learning by presenting users with quizzes at different difficulty levels (easy, medium, hard). It also tracks player scores, stores them in a database, and displays top results for each difficulty level. This allows for a more dynamic and personalized experience compared to my earlier projects, which were mainly informational or transactional.


# World Geography Quiz

This is a simple Django-based quiz application about world geography. The quiz consists of 10 questions per game and offers three difficulty levels: Easy, Medium, and Hard.

## Project Structure

final project/
│
├─ quiz/ # Django app
│ ├─ migrations/ # Database migrations
│ ├─ templates/quiz/ # HTML templates (start, question, result)
│ ├─ pycache/ # Python cache files
│ ├─ admin.py
│ ├─ apps.py
│ ├─ models.py
│ ├─ tests.py
│ ├─ urls.py
│ ├─ views.py
│ └─ init.py
├─ quizproject/ # Django project settings
│ ├─ pycache/
│ ├─ asgi.py
│ ├─ settings.py
│ ├─ urls.py
│ ├─ wsgi.py
│ └─ init.py
├─ db.sqlite3 # SQLite database with questions and scores
├─ manage.py
├─ requirements.txt
└─ README.md


## Requirements

- Python 3.8+
- Django >=3.2, <5.0

## Setup and Running the Project


This project already includes a pre-populated SQLite database (`db.sqlite3`) with quiz questions and some sample scores. This allows the quiz to run immediately without needing to manually add data.

1. Create and activate a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate   # Windows
source venv/bin/activate  # macOS/Linux


2. Install dependencies:

pip install -r requirements.txt

3. Run database migrations

python manage.py migrate

4. Create a superuser (optional, for admin access)

python manage.py createsuperuser

5. Start the development server

python manage.py runserver

6. Open your browser and navigate to:

http://127.0.0.1:8000/

to start the quiz

Notes

The db.sqlite3 database is included with pre-populated questions and scores for testing purposes.

All quiz logic, scoring, and session management are implemented in Django views.

This project is for educational purposes.



