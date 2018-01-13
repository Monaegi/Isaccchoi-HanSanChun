import re
import sys
from io import BytesIO
from urllib import request

from PIL import Image
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

__all__ = (
    'PersonalInfo',
    'MainImages',
    'WeightWorkOut',
)

CERTAIN_MUSCLE = (
    ('che', '가슴'),
    ('bac', '등'),
    ('shd', '어깨'),
    ('arm', '팔'),
    ('leg', '다리'),
    ('abd', '복부'),
    ('com', '복합'),
)


class PersonalInfo(models.Model):
    name = models.CharField(max_length=10)
    main_text = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=100)
    # fixme regex적용 필요
    phone_num = models.CharField(max_length=20)
    mail = models.EmailField()
    facebook_id = models.CharField(max_length=30)
    instagram_id = models.CharField(max_length=30)


class MainImages(models.Model):
    info = models.ForeignKey('PersonalInfo', on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='main')


class WeightWorkOut(models.Model):
    muscle = models.CharField(choices=CERTAIN_MUSCLE, max_length=3)
    name = models.CharField(max_length=20)
    description = models.TextField()
    url = models.URLField()
    thumbnail = models.ImageField(upload_to='thumbnail', blank=True)

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


@receiver(post_delete, sender=WeightWorkOut)
def post_delete(sender, instance, **kwargs):
    storage, path = instance.thumbnail.storage, instance.tumbnail.path
    if (path != '.') and (path != '/') and (path != 'photos/') and (path != 'photos/.'):
        storage.delete(path)
