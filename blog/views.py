from django.shortcuts import render

from .models import *


def index(request):
    person = PersonalInfo.objects.first()
    home_images = Home.objects.all()
    before_after = BeforeAfter.objects.all().order_by('?')[:6]
    categories = CategoryWorkOut.objects.all()

    ctx = {
        'person': person,
        'home_images': home_images,
        'before_after': before_after,
        'categories': categories,
    }
    return render(request, 'blog/index.html', ctx)
