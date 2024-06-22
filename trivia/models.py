from django.db import models
from django.contrib.auth.models import User

class Invitation(models.Model):
    from_user = models.ForeignKey(User, related_name='invitations_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='invitations_received', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invitation from {self.from_user} to {self.to_user}"

class Game(models.Model):
    player1 = models.ForeignKey(User, related_name='game_player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name='game_player2', on_delete=models.CASCADE)
    player1_score = models.IntegerField(default=0)
    player2_score = models.IntegerField(default=0)
    current_turn = models.IntegerField(null=True, blank=True)
    current_question = models.ForeignKey('Question', null=True, blank=True, on_delete=models.SET_NULL)
    rounds_played = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=[('ongoing', 'Ongoing'), ('finished', 'Finished')], default='ongoing')

    def __str__(self):
        return f"{self.player1} vs {self.player2} - {self.status}"

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text
