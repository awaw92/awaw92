# World Geography Quiz

## About This Project
This project is a **World Geography Quiz application** built with Django and JavaScript. Unlike my previous projects such as Submit Search, Wiki Commerce, and Mail Network, this project focuses on **interactive learning** by presenting users with quizzes at different difficulty levels (Easy, Medium, Hard). It tracks player scores, stores them in a database, and displays top results for each difficulty level, allowing for a more dynamic and personalized experience.

## Distinctiveness and Complexity
This project satisfies the distinctiveness and complexity requirements in several ways:  

- **Dynamic scoring system:** Player scores are stored in a Django model (`PlayerScore`) and ranked by difficulty level.  
- **Multiple difficulty levels:** Questions are categorized into Easy, Medium, and Hard, making the quiz adaptable for different users.  
- **Session management and interactivity:** Each quiz session tracks the user’s progress and score, providing a responsive experience.  
- **Front-end interactivity:** JavaScript is used for client-side functionality such as question navigation, timer management, and dynamic score updates.  
- **Mobile-responsive design:** The quiz layout adjusts for different screen sizes, ensuring usability on both desktop and mobile devices.  

These features make this project more advanced than previous CS50W projects, which were mostly informational or transactional, and clearly distinct from social networks or e-commerce sites.

## Project Structure

final project/
├─ quiz/ # Django app
│ ├─ migrations/ # Database migrations
│ ├─ templates/quiz/ # HTML templates: start, question, result
│ ├─ admin.py # Admin site registration
│ ├─ apps.py # App configuration
│ ├─ models.py # PlayerScore and question models
│ ├─ tests.py # Unit tests
│ ├─ urls.py # App URL routes
│ ├─ views.py # Quiz logic and scoring
│ └─ init.py
├─ quizproject/ # Django project settings
│ ├─ asgi.py
│ ├─ settings.py
│ ├─ urls.py
│ ├─ wsgi.py
│ └─ init.py
├─ db.sqlite3 # Pre-populated SQLite database with questions and scores
├─ manage.py # Django management script
├─ requirements.txt # Python package dependencies
└─ README.md


## Requirements
- Python 3.8+
- Django >=3.2, <5.0

## Setup and Running the Project
1. Create and activate a virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\activate   # Windows
source venv/bin/activate  # macOS/Linux

2. Install dependencies:

pip install -r requirements.txt


3. Run database migrations:

python manage.py migrate


4. (Optional) Create a superuser for admin access:

python manage.py createsuperuser

5. Start the development server:

python manage.py runserver

6. Open your browser and navigate to:

http://127.0.0.1:8000/       # Start the quiz
http://127.0.0.1:8000/admin  # Admin interface


Notes

The db.sqlite3 database is included with pre-populated questions and sample scores for immediate testing.

All quiz logic, scoring, and session management are implemented in Django views.

Front-end uses JavaScript for interactive question navigation and score tracking.

The project is mobile-responsive and adapts to different screen sizes.

This project is for educational purposes.