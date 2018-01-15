from django.shortcuts import render

from .models import *


def index(request):
    person = PersonalInfo.objects.first()
    home_images = Home.objects.all()
    workout = WeightWorkOut.objects.all()
    ctx = {
        'person': person,
        'home_images': home_images,
        'workout': workout,
    }
    return render(request, 'blog/index.html', ctx)
