from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='firstview'),
    path('<int:tournament_id>', views.firstview, name="firstview"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    # path('tournament', views.tournament, name='tournament'),
    # path('existing', views.existing, name="tourexisting"),
    path('choose', views.choose, name="choose"),
    path('choosetournament', views.choosetournament, name="choosetournament"),
    path('<int:tournament_id>/<int:level_id>/teams/', views.teams, name='teams'),
    path('<int:tournament_id>/<int:level_id>/', views.categories, name='category'),
    path('<int:tournament_id>/<int:level_id>/<int:category_id>/', views.questions, name='question'),
    path('<int:tournament_id>/<int:level_id>/<int:category_id>/<int:question_id>', views.specquestion, name='specquestion'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
]