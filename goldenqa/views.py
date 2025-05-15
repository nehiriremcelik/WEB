from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'cores/signup.html', {'form': form})

def home(request):
    all_tags = dict(Question.TAG_CHOICES)
    
    selected_tag = request.GET.get('tag')
    
    if selected_tag:
        questions = Question.objects.filter(tag=selected_tag).order_by('-created_at')
    else:
        questions = None  
    
    login_warning = None
    if request.method == 'POST':
        if not request.user.is_authenticated:
            form = QuestionForm(request.POST)
            login_warning = "You must be logged in to submit a question."
        else:
            form = QuestionForm(request.POST)
            if form.is_valid():
                q = form.save(commit=False)
                q.user = request.user
                q.save()
                return redirect('home')
    else:
        form = QuestionForm()
    
    return render(request, 'cores/home.html', {
        'questions': questions,
        'form': form,
        'all_tags': all_tags,
        'selected_tag': selected_tag,
        'login_warning': login_warning
    })


def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)

    # Check if the user is logged in
    if not request.user.is_authenticated:
        # If not authenticated, redirect to the 'must_login' page
        return render(request, 'cores/must_login.html')

    answers = question.answers.all().order_by('-created_at')
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.user = request.user
            a.question = question
            a.save()
            return redirect('question_detail', pk=pk)
    else:
        form = AnswerForm()
    return render(request, 'cores/question_detail.html', {'question': question, 'answers': answers, 'form': form})


@login_required
def like_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user in answer.likes.all():
        answer.likes.remove(request.user)
        liked = False
    else:
        answer.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'like_count': answer.likes.count()})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'cores/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')