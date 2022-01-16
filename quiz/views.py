from django.shortcuts import render, redirect
from .models import Quiz, Question, Option, UserMarks
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import QuizForm, QuestionForm
from django.forms import inlineformset_factory


def index(request):
    quiz = Quiz.objects.all()
    param = {'quiz': quiz}
    return render(request, "index.html", param)


@login_required(login_url='/login')
def quiz(request, id):
    quiz = Quiz.objects.get(id=id)
    return render(request, "quiz.html", {'quiz':quiz})


def quiz_data_view(request, id):
    quiz = Quiz.objects.get(id=id)
    questions = []
    for q in quiz.get_questions():
        options = []
        for a in q.get_options():
            options.append(a.content)
        questions.append({str(q): options})
    return JsonResponse({
        'data': questions,
        'time': quiz.duration,
    })


def save_quiz_view(request, id):
    if request.is_ajax():
        questions = []
        data = request.POST
        print("data: ", data)
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.get(content=k)
            questions.append(question)

        user = request.user
        quiz = Quiz.objects.get(id=id)

        score = 0
        marks = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.content)

            if a_selected != "":
                question_options = Option.objects.filter(question=q)
                for a in question_options:
                    if a_selected == a.content:
                        if a.correct:
                            score += 1
                            correct_answer = a.content
                    else:
                        if a.correct:
                            correct_answer = a.content

                marks.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                marks.append({str(q): 'not answered'})

        UserMarks.objects.create(quiz=quiz, user=user, score=score)

        return JsonResponse({'passed': True, 'score': score, 'marks': marks})


def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password1']
        confirm_password = request.POST['password2']

        if password != confirm_password:
            return redirect('/signup')

        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return redirect('/login')
        # return render(request, 'login.html')
    return render(request, "signup.html")


def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("/")
        else:
            return render(request, "login.html")
    return render(request, "login.html")


def logout(request):
    auth_logout(request)
    return redirect('/')


def add_quiz(request):
    quizzes = Quiz.objects.filter().order_by('-id')

    if request.method=="POST":
        form = QuizForm(data=request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.save()
            print("quiz: ", quiz)
            obj = form.instance
            print("obj: ", obj)
            return render(request, "add_quiz.html", {'form':form, 'quizzes':quizzes})
    else:
        form=QuizForm()
    return render(request, "add_quiz.html", {'form':form, 'quizzes':quizzes})


def add_question(request):
    questions = Question.objects.filter().order_by('-id')
    if request.method=="POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "add_question.html", {'form':form, 'questions':questions})
    else:
        form=QuestionForm()
    return render(request, "add_question.html", {'form':form, 'questions':questions})


def delete_question(request, id):
    question = Question.objects.get(id=id)
    if request.method == "POST":
        question.delete()
        return redirect('/add_question/')
    return render(request, "delete_question.html", {'question':question})


def delete_quiz(request, id):
    quiz = Quiz.objects.get(id=id)
    if request.method == "POST":
        quiz.delete()
        return redirect('/add_quiz/')
    return render(request, "delete_quiz.html", {'quiz':quiz})


def add_options(request, id):
    question = Question.objects.get(id=id)
    QuestionFormSet = inlineformset_factory(Question, Option, fields=('content','correct', 'question'), extra=4)
    if request.method=="POST":
        formset = QuestionFormSet(request.POST, instance=question)
        if formset.is_valid():
            formset.save()
            alert = True
            return render(request, "add_options.html", {'alert':alert})
    else:
        formset=QuestionFormSet(instance=question)
    return render(request, "add_options.html", {'formset':formset, 'question':question})


def results(request):
    marks = UserMarks.objects.all()
    return render(request, "results.html", {'marks':marks})


def delete_result(request, id):
    marks = UserMarks.objects.get(id=id)
    if request.method == "POST":
        marks.delete()
        return redirect('/results/')
    return render(request, "delete_result.html", {'marks':marks})