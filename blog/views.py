from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

from .forms import QuestionForm
from .models import *


def index(request):
    if request.method == 'GET':
        question_form = QuestionForm
    else:
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question_form.save()
            return redirect('index')
    person = PersonalInfo.objects.first()
    home_images = Home.objects.all()
    before_after = BeforeAfter.objects.all().order_by('?')[:6]
    categories = CategoryWorkOut.objects.all()
    question_paginator = Paginator(Question.objects.all(), 10)

    page = request.GET.get('page')

    try:
        question = question_paginator.page(page)
    except PageNotAnInteger:
        question = question_paginator.page(1)
    except EmptyPage:
        question = question_paginator.page(question_paginator.num_pages)

    ctx = {
        'person': person,
        'home_images': home_images,
        'before_after': before_after,
        'categories': categories,
        'questions': question,
        'question_form': question_form,
    }
    return render(request, 'blog/index.html', ctx)
