from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.contrib.auth.decorators import login_required

def home(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'QandAGramApp/home.html', {'questions': questions})

@login_required
def post_question(request):
    form = QuestionForm(request.POST or None)
    if form.is_valid():
        question = form.save(commit=False)
        question.user = request.user
        question.save()
        return redirect('home')
    return render(request, 'QandAGramApp/post_question.html', {'form': form})

def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = question.answers.all()
    form = AnswerForm()
    return render(request, 'QandAGramApp/question_detail.html', {
        'question': question,
        'answers': answers,
        'form': form
    })

@login_required
def post_answer(request, pk):
    question = get_object_or_404(Question, pk=pk)
    form = AnswerForm(request.POST)
    if form.is_valid():
        answer = form.save(commit=False)
        answer.question = question
        answer.user = request.user
        answer.save()
    return redirect('question_detail', pk=pk)

@login_required
def like_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    if request.user in answer.likes.all():
        answer.likes.remove(request.user)
    else:
        answer.likes.add(request.user)
    return redirect('question_detail', pk=answer.question.pk)

@login_required
def my_questions(request):
    user_questions = Question.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'QandAGramApp/my_questions.html', {'questions': user_questions})