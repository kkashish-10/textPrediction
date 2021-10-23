from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class text(models.Model):
    content=RichTextField(blank=True, null=True)