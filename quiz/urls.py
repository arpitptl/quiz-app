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

    path('add_quiz/', views.add_quiz, name='add_quiz'),
    path('add_question/', views.add_question, name='add_question'),
    path('add_options/<int:id>/', views.add_options, name='add_options'),
    path('delete_question/<int:id>/', views.delete_question, name='delete_question'),
]