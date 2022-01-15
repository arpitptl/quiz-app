from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:id>/", views.quiz, name="quiz"),
    path('<int:id>/data/', views.quiz_data_view, name='quiz-data'),
    path('<int:id>/save/', views.save_quiz_view, name='quiz-save'),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
]