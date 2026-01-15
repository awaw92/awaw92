from django.db import models

class Question(models.Model):
    LEVEL_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    question_text = models.CharField(max_length=200)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    correct_option = models.PositiveSmallIntegerField()  # numer poprawnej odpowiedzi: 1, 2, 3 lub 4
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)

    def __str__(self):
        return f"{self.question_text} ({self.level})"


class PlayerScore(models.Model):
    LEVEL_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    score = models.PositiveIntegerField()
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='easy')  # domyślny poziom
    date = models.DateTimeField(auto_now_add=True)  # zapis daty wykonania quizu

    def __str__(self):
        return f"{self.name} - {self.score} points ({self.level})"
