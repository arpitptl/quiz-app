from django import forms
from .models import Quiz, Question
from django.contrib import admin


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = "__all__"


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"

