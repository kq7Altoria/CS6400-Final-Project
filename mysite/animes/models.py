import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User

# Create your models here.
class User(AbstractUser):
    pass

class AnimeWork(models.Model):
    anime_id = models.AutoField(primary_key = True)
    anime_name = models.CharField(max_length = 300)
    anime_description = models.CharField(max_length = 10000)
    anime_avatar_url = models.CharField(max_length = 300, default = None)
    anime_cover_image_url = models.CharField(max_length = 300, default = None)
    anime_rating = models.DecimalField(max_digits = 4, decimal_places = 2)
    anime_airing_start_date = models.DateField()
    anime_airing_end_date = models.DateField()

    def __str__(self):
        return self.anime_name

class Tag(models.Model):
    tag_anime_id = models.ManyToManyField(AnimeWork)
    tag_name = models.CharField(max_length = 50)

class ProductionCompany(models.Model):
    company_name = models.CharField(max_length = 50)
    company_anime_id = models.ManyToManyField(AnimeWork)

class Review(models.Model):
    review_id = models.AutoField(primary_key = True)
    review_anime_id = models.ForeignKey(AnimeWork, on_delete=models.CASCADE)
    review_content = models.CharField(max_length = 10000)
    review_date_created = models.DateTimeField(auto_now_add = True)
    review_date_modified = models.DateTimeField(auto_now = True)
    review_upvotes = models.IntegerField(default = 0)
    reviewer_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering =  ['review_date_created']

    def __str__(self):
        return self.review_date_modified

class Reply(models.Model):
    reply_id = models.AutoField(primary_key = True)
    parent_review_id = models.ForeignKey(Review, on_delete=models.CASCADE)
    reply_date_created = models.DateTimeField(auto_now_add = True)
    reply_date_modified = models.DateTimeField(auto_now = True)
    replyer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_upvotes = models.IntegerField(default = 0)
    reply_content = models.CharField(max_length = 10000)

    class Meta:
        ordering = ['reply_date_created']

    def __str__(self):
        return self.review_date_modified
