import re
import sys
from io import BytesIO
from urllib import request

import requests
from PIL import Image
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

__all__ = (
    'PersonalInfo',
    'Home',
    'CategoryWorkOut',
    'WeightWorkOut',
    'BeforeAfter',
    'Question',
    'Comment',
)

CERTAIN_MUSCLE = (
    ('chest', '가슴'),
    ('back', '등'),
    ('shoulder', '어깨'),
    ('arm', '팔'),
    ('leg', '다리'),
    ('abdomen', '복부'),
    ('complex', '복합'),
)


class PersonalInfo(models.Model):
    name = models.CharField(max_length=10)
    image = models.ImageField(upload_to='profile_image', null=True, blank=True)
    description = models.TextField()
    address = models.CharField(max_length=100)
    latitude = models.FloatField(blank=True)
    longitude = models.FloatField(blank=True)
    # fixme regex적용 필요
    phone_num = models.CharField(max_length=20)
    mail = models.EmailField()
    facebook_id = models.CharField(max_length=30)
    instagram_id = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.latitude and not self.longitude:
            params = {
                'address': self.address,
            }
            res = requests.get(settings.GOOGLE_MAPS_API_URL, params=params).json()
            location = res['results'][0]['geometry']['location']
            lat = location['lat']
            lng = location['lng']
            try:
                lat = float(lat)
                lng = float(lng)
            except ValueError:
                lat = 1
                lng = 1
            except TypeError:
                lat = 1
                lng = 1
            finally:
                self.latitude = lat
                self.longitude = lng
        return super().save(*args, **kwargs)


class Home(models.Model):
    image = models.ImageField(upload_to='main')
    text = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.text[0:11]} - {self. pk}'


class BeforeAfter(models.Model):
    image = models.ImageField(upload_to='before_after')
    period = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.image.name.split('/')[1]} - {self.period}"


class CategoryWorkOut(models.Model):
    name = models.CharField(choices=CERTAIN_MUSCLE, max_length=8)
    image = models.ImageField(upload_to='category')
    image_thumbnail = ImageSpecField(source='image',
                               processors=[ResizeToFill(440, 200)],
                               format='JPEG',
                               options={'quality': 60})

    def __str__(self):
        return self.get_name_display()


class WeightWorkOut(models.Model):
    category = models.ForeignKey('CategoryWorkOut', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.TextField()
    url = models.URLField()
    thumbnail = models.ImageField(upload_to='thumbnail', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        pattern = re.compile(
            r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/ ]{11})',
            re.IGNORECASE)
        url = self.url
        match = re.search(pattern, url)
        youtube_id = match.group(1)
        if youtube_id is None:
            raise ValidationError
        src = f"https://img.youtube.com/vi/{ youtube_id }/0.jpg"
        result = request.urlretrieve(src)
        image = Image.open(result[0])
        output = BytesIO()
        resize_image = image.resize((300, 200))
        resize_image.save(output, format='JPEG', quality=100)
        output.seek(0)
        self.thumbnail = InMemoryUploadedFile(output, 'ImageField', f'{youtube_id}.jpg', 'image/jpeg',
                                              sys.getsizeof(output), None)
        return super().save(*args, **kwargs)


class Question(models.Model):
    name = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField()
    phone_regex = RegexValidator(regex=r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$',
                                 message="전화번호는 '010-1234-5678'혹은 '01012345678'형태로 입력하여야 합니다.")
    phone_number = models.CharField(validators=[phone_regex], max_length=13)
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.name} - {self.title}'


class Comment(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'comment | {self.question.name} - {self.question.title}'


@receiver(post_delete, sender=WeightWorkOut)
def workout_delete(sender, instance, **kwargs):
    storage, path = instance.thumbnail.storage, instance.thumbnail.path
    if (path != '.') and (path != '/') and (path != 'photos/') and (path != 'photos/.'):
        storage.delete(path)


@receiver(post_delete, sender=PersonalInfo)
def info_delete(sender, instance, **kwargs):
    storage, path = instance.image.storage, instance.image.path
    if (path != '.') and (path != '/') and (path != 'photos/') and (path != 'photos/.'):
        storage.delete(path)
