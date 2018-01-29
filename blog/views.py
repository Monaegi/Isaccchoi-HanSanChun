from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404

from .forms import QuestionForm, CommentForm
from .models import *


def index(request):
    if request.method == "POST":
        form_type = request.POST.get('type', None)
        if form_type is None:
            raise ValueError("폼 타입이 확인되지 않습니다.")
        if form_type == "question":
            question_form = QuestionForm(request.POST)
            if question_form.is_valid():
                question_form.save()
                return redirect('/#qa')
        elif form_type == "comment":
            question_id = request.POST.get('question_id', None)
            if question_id is None:
                raise ValueError("질문 번호가 확인되지 않습니다.")
            post_question = get_object_or_404(Question, id=question_id)
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.question = post_question
                comment_form.save()
                return redirect('/#qa')

    if 'comment_form' not in locals():
        comment_form = CommentForm
    if 'question_form' not in locals():
        question_form = QuestionForm

    person = PersonalInfo.objects.first()
    home_images = Home.objects.all()
    before_after = BeforeAfter.objects.all().order_by('?')[:6]
    categories = CategoryWorkOut.objects.all().order_by('-id')
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
        'comment_form': comment_form,
    }
    return render(request, 'blog/index.html', ctx)
