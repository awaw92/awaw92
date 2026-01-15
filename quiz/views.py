from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, PlayerScore
import random

# Widok startowy - formularz z imieniem, krajem, wiekiem i poziomem trudności
def start_quiz(request):
    if request.method == "POST":
        # zapisujemy dane gracza w sesji
        request.session['player_name'] = request.POST.get('player_name')
        request.session['player_country'] = request.POST.get('player_country')
        request.session['player_age'] = request.POST.get('player_age')
        request.session['level'] = request.POST.get('level')  # poziom trudności
        request.session['score'] = 0  # startujemy punktację od zera
        request.session['current_index'] = 0  # indeks bieżącego pytania
        request.session['quiz_answers'] = []  # lista odpowiedzi gracza
        request.session['score_saved'] = False  # flaga, czy wynik został zapisany

        # pobieramy wszystkie pytania z wybranego poziomu
        questions = list(Question.objects.filter(level=request.session['level']))
        if len(questions) < 1:
            return render(request, 'quiz/start.html', {
                'error': 'Brak pytań w wybranym poziomie trudności.'
            })

        # losujemy maksymalnie 10 pytań
        random.shuffle(questions)
        request.session['question_ids'] = [q.id for q in questions[:10]]

        # przekierowanie do pierwszego pytania
        first_question_id = request.session['question_ids'][0]
        return redirect('quiz:question', question_id=first_question_id)

    return render(request, 'quiz/start.html')


# Widok pojedynczego pytania
def question_view(request, question_id):
    question_ids = request.session.get('question_ids', [])
    current_index = request.session.get('current_index', 0)

    if current_index >= len(question_ids):
        return redirect('quiz:result')

    question = get_object_or_404(Question, id=question_ids[current_index])

    if request.method == "POST":
        selected_option = int(request.POST.get("option"))

        if 'score' not in request.session:
            request.session['score'] = 0

        if selected_option == question.correct_option:
            request.session['score'] += 1

        options = [question.option1, question.option2, question.option3, question.option4]
        your_answer_text = options[selected_option - 1]
        correct_answer_text = options[question.correct_option - 1]

        quiz_answers = request.session.get('quiz_answers', [])
        quiz_answers.append({
            'text': question.question_text,
            'your_answer': your_answer_text,
            'correct_answer': correct_answer_text
        })
        request.session['quiz_answers'] = quiz_answers

        request.session['current_index'] += 1
        if request.session['current_index'] < len(question_ids):
            next_question_id = question_ids[request.session['current_index']]
            return redirect('quiz:question', question_id=next_question_id)
        else:
            return redirect('quiz:result')

    return render(request, 'quiz/question.html', {'question': question})


# Widok końcowy - wynik gracza
def result_view(request):
    score = request.session.get('score', 0)
    player_name = request.session.get('player_name', 'Player')
    player_country = request.session.get('player_country', '')
    player_age = request.session.get('player_age', 0)
    level = request.session.get('level', 'easy')  # pobieramy poziom trudności z sesji
    total_questions = len(request.session.get('question_ids', []))
    questions = request.session.get('quiz_answers', [])

    # zapis wyniku tylko raz
    if not request.session.get('score_saved', False):
        PlayerScore.objects.create(
            name=player_name,
            country=player_country,
            age=player_age,
            score=score,
            level=level
        )
        request.session['score_saved'] = True

    # Pobieramy top 5 wyników tylko dla bieżącego poziomu trudności
    top_scores = PlayerScore.objects.filter(level=level).order_by('-score', 'date')[:5]

    return render(request, 'quiz/result.html', {
        'player_name': player_name,
        'score': score,
        'total_questions': total_questions,
        'questions': questions,
        'top_scores': top_scores
    })
