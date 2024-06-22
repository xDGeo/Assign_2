from django.contrib import admin
from .models import Invitation, Game, Question

admin.site.register(Invitation)
admin.site.register(Game)
admin.site.register(Question)
