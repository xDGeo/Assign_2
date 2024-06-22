from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('invite/', views.invite, name='invite'),
    path('accept_invitation/<int:invite_id>/', views.accept_invitation, name='accept_invitation'),
    path('reject_invitation/<int:invite_id>/', views.reject_invitation, name='reject_invitation'),  # Ensure this is included
    path('game/<int:game_id>/', views.game_view, name='game'),
    path('result/<int:game_id>/', views.result, name='result'),
    path('', views.home, name='home'),
]
