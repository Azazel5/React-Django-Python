from django.db import models
from django.contrib.auth.models import User

class UserImages(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='UserImages', null=True)

    class Meta:
        verbose_name = 'UserImage'

    def __str__(self):
        return f'ImgTitle - {self.title}'
    