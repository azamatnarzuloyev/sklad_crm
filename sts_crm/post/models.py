from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.



class Istoriya(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="image",blank=True, null=True)
    video = models.FileField(upload_to="video", blank=True, null=True)
    text = RichTextField()
   