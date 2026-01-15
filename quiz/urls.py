from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.start_quiz, name='start_quiz'),  # startowy formularz z imieniem, krajem i wiekiem
    path('question/<int:question_id>/', views.question_view, name='question'),  # widok pojedynczego pytania
    path('result/', views.result_view, name='result'),  # widok końcowy z wynikiem
]
