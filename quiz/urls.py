from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    # Quiz related urls
    path("<int:id>/", views.quiz, name="quiz"),
    path('<int:id>/data/', views.quiz_data_view, name='quiz-data'),
    path('<int:id>/save/', views.save_quiz_view, name='quiz-save'),
    path('add_quiz/', views.add_quiz, name='add_quiz'),
    path('delete_quiz/<int:id>/', views.delete_quiz, name='delete_quiz'),

    # User authentication and registration related urls
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),

    # Questions related urls
    path('add_question/', views.add_question, name='add_question'),
    path('delete_question/<int:id>/', views.delete_question, name='delete_question'),

    # Options related urls
    path('add_options/<int:id>/', views.add_options, name='add_options'),

    # User's result related utls
    path('results/', views.results, name='results'),
    path('delete_result/<int:id>/', views.delete_result, name='delete_result'),
]