from django.shortcuts import render

from .models import *


def index(request):
    person = PersonalInfo.objects.first()
    home_images = Home.objects.all()
    workout = WeightWorkOut.objects.all()
    before_after = BeforeAfter.objects.all().order_by('?')[:6]

    ctx = {
        'person': person,
        'home_images': home_images,
        'workout': workout,
        'before_after': before_after,
    }
    return render(request, 'blog/index.html', ctx)
