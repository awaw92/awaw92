World Geography Quiz – CS50W Final Project
Overview

World Geography Quiz is a full-stack web application built with Django, Python, and JavaScript, designed as an interactive learning platform for testing and improving world geography knowledge. Users take a quiz consisting of randomly selected questions, choose a difficulty level, and receive immediate feedback, final results, and a ranked leaderboard.

This project was created as the Final Capstone Project for CS50’s Web Programming with Python and JavaScript and demonstrates the integration of backend logic, database models, session management, and dynamic front-end behavior.

Distinctiveness and Complexity

This project satisfies the distinctiveness and complexity requirements of the CS50W Capstone in the following concrete ways:

What this project is

This application is an interactive quiz system that combines:

persistent user score tracking,

difficulty-based content filtering,

session-based quiz progression,

real-time client-side interactivity,

and database-driven ranking.

Unlike earlier course projects that focused on CRUD operations, social interactions, or transactional workflows, this project emphasizes stateful user interaction, game-like progression, and educational feedback loops.

Key aspects of complexity

Session-Based Quiz Flow
The application maintains quiz state entirely through Django sessions, tracking:

current question index,

selected answers,

accumulated score,

and quiz completion state.

This ensures a controlled multi-step workflow without user authentication.

Dynamic Difficulty Levels
Questions are categorized into Easy, Medium, and Hard.
Each quiz session dynamically selects and randomizes up to 10 questions from the chosen difficulty level.

Persistent Scoring and Rankings
Player results are stored in a database model (PlayerScore) and ranked per difficulty level, allowing comparison between different quiz attempts.

Client-Side Interactivity with JavaScript
JavaScript is used to:

handle answer selection,

visually indicate correct and incorrect answers,

delay form submission for animations,

and improve user experience beyond standard Django form handling.

Separation of Concerns
The project cleanly separates:

database models,

view logic,

templates,

and client-side behavior.

Together, these elements make the project substantially more complex than earlier assignments and clearly distinct in both purpose and implementation.

Project Structure and File Descriptions
quiz/models.py

Defines the database schema:

Question model
Stores quiz questions, four answer options, the correct answer index, and difficulty level.

PlayerScore model
Stores player name, country, age, score, difficulty level, and timestamp for ranking purposes.

These models enable persistent quiz content and historical score tracking.

quiz/views.py

Contains all core quiz logic:

start_quiz
Handles quiz initialization, player data collection, session setup, question selection, and difficulty filtering.

question_view
Manages individual quiz questions, validates answers, updates score, and tracks quiz progress.

result_view
Displays the final score, detailed answer summary, and saves the player’s result to the database only once per session.

This file is the backbone of application logic and session management.

quiz/templates/quiz/start.html

The quiz entry point:

Collects player name, country, age, and difficulty level.

Includes validation and error handling for missing questions.

Provides a clean, mobile-responsive UI.

quiz/templates/quiz/question.html

Displays individual quiz questions:

Uses JavaScript to handle answer selection.

Highlights correct and incorrect answers visually.

Prevents multiple submissions.

Uses animations for smooth user experience.

Submits answers asynchronously after visual feedback.

quiz/templates/quiz/result.html

Displays final quiz results:

Shows total score and number of questions.

Provides a detailed question-by-question summary.

Highlights correct and incorrect answers.

Displays a leaderboard filtered by difficulty level.

Highlights the current player’s result if present in the top scores.

quiz/urls.py

Defines URL routing for:

quiz start page,

question navigation,

result page.

quiz/admin.py

Registers models with the Django admin interface, allowing quiz questions and scores to be managed via the admin panel.

quizproject/settings.py

Contains standard Django project configuration:

installed apps,

middleware,

database configuration (SQLite),

template settings,

static files configuration.

db.sqlite3

Pre-populated SQLite database containing:

sample quiz questions,

example player scores.

This allows immediate testing without manual data entry.

requirements.txt

Lists required Python dependencies, including Django.

Setup and Running the Project
Requirements

Python 3.8+

Django >= 3.2 and < 5.0

Installation Steps

Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows


Install dependencies:

pip install -r requirements.txt


Apply database migrations:

python manage.py migrate


(Optional) Create an admin user:

python manage.py createsuperuser


Run the development server:

python manage.py runserver


Open in browser:

Quiz application: http://127.0.0.1:8000/

Admin panel: http://127.0.0.1:8000/admin/

Additional Notes

All quiz logic and scoring is handled server-side using Django sessions.

JavaScript is used exclusively to enhance user interaction and feedback.

The application is fully responsive and works on mobile and desktop devices.

This project was developed solely for educational purposes as part of CS50W.

Conclusion

This project demonstrates a complete Django web application that integrates backend logic, persistent storage, session management, and interactive front-end behavior. Its structure, features, and implementation clearly satisfy the distinctiveness and complexity requirements of the CS50 Web Programming Final Project.