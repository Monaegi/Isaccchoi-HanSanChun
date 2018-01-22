from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .forms import QuestionForm
from .models import *


def index(request):
    person = PersonalInfo.objects.first()
    home_images = Home.objects.all()
    before_after = BeforeAfter.objects.all().order_by('?')[:6]
    categories = CategoryWorkOut.objects.all()
    question = Question.objects.all()
    question_form = QuestionForm

    ctx = {
        'person': person,
        'home_images': home_images,
        'before_after': before_after,
        'categories': categories,
        'question': question,
        'question_form': question_form,
    }
    return render(request, 'blog/index.html', ctx)


@require_POST
def question_create(request):
    form = QuestionForm(request.POST)

    if form.is_valid():
        form.save()
    return redirect('index')
