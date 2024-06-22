import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Invitation, Game, Question
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
import json
from django.http import JsonResponse


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'trivia/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'trivia/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def home(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        invitations = request.user.invitations_received.all()
        games = Game.objects.filter(player1=request.user, status='ongoing') | Game.objects.filter(player2=request.user, status='ongoing')
        unique_games = games.distinct()
        games_with_opponent = [
            {
                'game': game,
                'opponent': game.player1 if game.player1 != request.user else game.player2
            }
            for game in unique_games
        ]
        invitations_data = [
            {
                'id': invitation.id,
                'from_user': {
                    'username': invitation.from_user.username
                }
            }
            for invitation in invitations
        ]
        games_data = [
            {
                'game': {
                    'id': game['game'].id
                },
                'opponent': {
                    'username': game['opponent'].username
                }
            }
            for game in games_with_opponent
        ]
        return JsonResponse({'invitations': invitations_data, 'games_with_opponent': games_data})
    else:
        invitations = request.user.invitations_received.all()
        games = Game.objects.filter(player1=request.user, status='ongoing') | Game.objects.filter(player2=request.user, status='ongoing')
        unique_games = games.distinct()
        games_with_opponent = [
            {
                'game': game,
                'opponent': game.player1 if game.player1 != request.user else game.player2
            }
            for game in unique_games
        ]
        return render(request, 'trivia/home.html', {'invitations': invitations, 'games_with_opponent': games_with_opponent})


@login_required
def invite(request):
    if request.method == 'POST':
        username = request.POST['username']
        try:
            to_user = User.objects.get(username=username)
            if to_user != request.user:
                Invitation.objects.create(from_user=request.user, to_user=to_user)
        except User.DoesNotExist:
            pass
        return JsonResponse({'status': 'ok'})
    return redirect('home')

@login_required
def accept_invitation(request, invite_id):
    invitation = get_object_or_404(Invitation, id=invite_id)
    if invitation.to_user == request.user:
        game = Game.objects.create(player1=invitation.from_user, player2=invitation.to_user)
        invitation.delete()
        return JsonResponse({'redirect': True, 'url': f'/game/{game.id}/'})
    return redirect('home')

@login_required
def reject_invitation(request, invite_id):
    invitation = get_object_or_404(Invitation, id=invite_id)
    if invitation.to_user == request.user:
        invitation.delete()
        return JsonResponse({'status': 'ok'})
    return redirect('home')

@login_required
def game_view(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if request.user not in [game.player1, game.player2]:
        return redirect('home')

    if game.status == 'finished':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'redirect': True, 'url': f'/result/{game.id}/'})
        return redirect('result', game_id=game.id)

    if game.current_turn is None:
        game.current_turn = 1  # Assuming 1 is player1's turn and 2 is player2's turn
        game.save()

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if request.method == 'POST':
        answer = request.POST['answer']
        if answer.lower().strip() == game.current_question.answer.lower().strip():
            if request.user == game.player1:
                game.player1_score += 1
            else:
                game.player2_score += 1
        game.rounds_played += 1

        if game.rounds_played >= 9 or game.player1_score == 5 or game.player2_score == 5:
            game.status = 'finished'
            game.save()
            if is_ajax:
                return JsonResponse({'redirect': True, 'url': f'/result/{game.id}/'})
            return redirect('result', game_id=game.id)
        else:
            game.current_turn = 2 if game.current_turn == 1 else 1
            game.current_question = None
            game.save()
            if is_ajax:
                return JsonResponse({'next_turn': True, 'current_turn': game.current_turn})

    if not game.current_question:
        questions = list(Question.objects.all())
        if questions:
            game.current_question = random.choice(questions)
            game.save()
        else:
            if is_ajax:
                return JsonResponse({'no_questions': True})
            return render(request, 'trivia/no_questions.html')

    if is_ajax:
        return JsonResponse({
            'question': game.current_question.question_text if game.current_question else '',
            'player1_score': game.player1_score,
            'player2_score': game.player2_score,
            'current_turn': game.current_turn,
        })

    return render(request, 'trivia/game.html', {'game': game})


@login_required
def result(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if game.status != 'finished':
        game.status = 'finished'
        game.save()

    if game.player1_score == game.player2_score:
        result_text = 'It\'s a draw!'
    elif game.player1_score > game.player2_score:
        result_text = f'{game.player1.username} wins!'
    else:
        result_text = f'{game.player2.username} wins!'

    return render(request, 'trivia/result.html', {'game': game, 'result_text': result_text})





