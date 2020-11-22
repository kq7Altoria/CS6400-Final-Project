import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days = 1) <= self.pub_date <=  now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Publised recently?'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length = 200)
    votes = models.IntegerField(default = 0)
    def __str__(self):
        return self.choice_text

class User(models.Model):
    user_id = models.IntegerField(primary_key = True)
    user_name = models.CharField(max_length = 25)
    user_cookie = models.CharField(max_length = 300)
    user_email = models.CharField(max_length = 50)
    user_avatar_url = models.CharField(max_length = 300)

class AnimeWork(models.Model):
    anime_id = models.IntegerField(primary_key = True)
    anime_name = models.CharField(max_length = 50)
    anime_description = models.CharField(max_length = 500)
    anime_avatar_url = models.CharField(max_length = 300)
    anime_cover_image_url = models.CharField(max_length = 300)
    anime_rating = models.DecimalField(max_digits = 4, decimal_places = 2)
    anime_aring_start_date = models.DateTimeField()
    anime_aring_end_date = models.DateTimeField()

class Tag(models.Model):
    tag_anime_id = models.ForeignKey(AnimeWork, on_delete=models.CASCADE)
    tag_name = models.CharField(max_length = 50)

class ProductionCompany(models.Model):
    company_name = models.CharField(max_length = 50)
    company_anime_id = models.ForeignKey(AnimeWork, on_delete=models.CASCADE)

class Review(models.Model):
    review_id = models.IntegerField(primary_key = True)
    review_anime_id = models.ForeignKey(AnimeWork, on_delete=models.CASCADE)
    review_content = models.CharField(max_length = 10000)
    review_date_created = models.DateTimeField(auto_now_add = True)
    review_date_modified = models.DateTimeField(auto_now = True)
    review_upvotes = models.IntegerField(default = 0)
    reviewer_id = models.ForeignKey(User, on_delete=models.CASCADE)
