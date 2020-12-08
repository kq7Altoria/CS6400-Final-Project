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
    anime_avatar_url = models.CharField(max_length = 300, default = "www.google.com")
    anime_cover_image_url = models.CharField(max_length = 300, default = "www.google.com")
    anime_rating = models.DecimalField(max_digits = 4, decimal_places = 2)
    anime_airing_start_date = models.CharField(max_length = 50, default = '')
    anime_airing_end_date = models.CharField(max_length = 50, default = '')

    def __str__(self):
        return self.anime_name

class WatchList(models.Model):
    user = models.OneToOneField(
    User, on_delete = models.CASCADE,
    )
    anime_works = models.ManyToManyField(AnimeWork)

class WishList(models.Model):
    user = models.OneToOneField(
    User, on_delete = models.CASCADE,
    )
    anime_works = models.ManyToManyField(AnimeWork)

class Tag(models.Model):
    tag_name = models.CharField(max_length = 50)
    tag_anime_works = models.ManyToManyField(AnimeWork)
    def __str__(self):
        return self.tag_name

class ProductionCompany(models.Model):
    company_name = models.CharField(max_length = 50)
    company_anime_works = models.ManyToManyField(AnimeWork)

    def __str__(self):
        return self.company_name

class Review(models.Model):
    review_id = models.AutoField(primary_key = True)
    review_anime_id = models.ForeignKey(AnimeWork, on_delete=models.CASCADE)
    review_content = models.CharField(max_length = 10000, default = '')
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
    reply_content = models.CharField(max_length = 10000, default = '')

    class Meta:
        ordering = ['reply_date_created']

    def __str__(self):
        return self.review_date_modified
