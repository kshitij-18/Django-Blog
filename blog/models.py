from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class article(models.Model):
    category_choices = (
        ('Public', 'Public'),
        ('Private', 'Private')
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=50, default="")
    description = models.TextField()
    article_image = models.ImageField(upload_to='blog/images', blank=True)
    category = models.CharField(
        max_length=10, choices=category_choices, default="Public")

    def __str__(self):
        return self.title
