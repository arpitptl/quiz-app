from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    number_of_questions = models.IntegerField(default=1)
    duration = models.IntegerField(help_text="Duration of the quiz in seconds", default="60")

    def __str__(self):
        return self.name

    def get_questions(self):
        return self.questions.all()


class Question(models.Model):
    content = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.content

    def get_answers(self):
        return self.options.all()


class Option(models.Model):
    content = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')

    def __str__(self):
        return f"question: {self.question.content}, option: {self.content}, correct: {self.correct}"


class UserMarks(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return str(self.quiz)


