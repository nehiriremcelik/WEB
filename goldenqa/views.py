from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Answer, Upvote, Downvote
from .forms import QuestionForm, AnswerForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Count, F
from django.db.utils import IntegrityError


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                return redirect('login')
            except IntegrityError:
                form.add_error('username', 'This username already exists. Please choose a different one.')
    else:
        form = SignUpForm()
    return render(request, 'cores/signup.html', {'form': form})

def home(request):
    all_tags = dict(Question.TAG_CHOICES)
    
    selected_tag = request.GET.get('tag')
    sort_by = request.GET.get('sort', 'new')  # Default to 'new'
    
    if selected_tag:
        questions = Question.objects.filter(tag=selected_tag).annotate(
            answer_count=Count('answers')
        )
        
        if sort_by == 'best':
            questions = questions.order_by('-answer_count', '-created_at')
        else:  # 'new'
            questions = questions.order_by('-created_at')
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
        'login_warning': login_warning,
        'sort_by': sort_by
    })


def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    
    answers = Answer.objects.filter(question=question).annotate(
        upvotes_count=Count('upvotes'),
        downvotes_count=Count('downvotes')
    ).annotate(
        score=F('upvotes_count') - F('downvotes_count')
    ).order_by('-score')
    
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.user = request.user
            answer.save()
            return redirect('question_detail', question_id=question_id)
    else:
        form = AnswerForm()

    user_upvotes = Upvote.objects.filter(user=request.user).values_list('answer_id', flat=True)
    user_downvotes = Downvote.objects.filter(user=request.user).values_list('answer_id', flat=True)

    answers_data = []
    for answer in answers:
        answers_data.append({
            'answer': answer,
            'score': answer.score,
            'is_upvoted': answer.id in user_upvotes,
            'is_downvoted': answer.id in user_downvotes
        })
    
    return render(request, 'cores/question_detail.html', {
        'question': question,
        'answers': answers,
        'answers_data': answers_data,
        'form': form,
        'user_upvotes': user_upvotes,
        'user_downvotes': user_downvotes
    })


@login_required
@require_POST
def vote_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    user = request.user
    action = request.POST.get('action')

    if action not in ['upvote', 'downvote']:
        return JsonResponse({'error': 'Invalid action'}, status=400)

    current_upvote = Upvote.objects.filter(answer=answer, user=user).first()
    current_downvote = Downvote.objects.filter(answer=answer, user=user).first()

    if action == 'upvote':
        if current_upvote:
            current_upvote.delete()
            user_vote = None
        else:
            if current_downvote:
                current_downvote.delete()
            Upvote.objects.create(answer=answer, user=user)
            user_vote = 'upvote'
    else:
        if current_downvote:
            current_downvote.delete()
            user_vote = None
        else:
            if current_upvote:
                current_upvote.delete()
            Downvote.objects.create(answer=answer, user=user)
            user_vote = 'downvote'

    upvotes_count = Upvote.objects.filter(answer=answer).count()
    downvotes_count = Downvote.objects.filter(answer=answer).count()
    vote_score = upvotes_count - downvotes_count

    return JsonResponse({
        'score': vote_score,
        'upvotes': upvotes_count,
        'downvotes': downvotes_count,
        'user_vote': user_vote
    })

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