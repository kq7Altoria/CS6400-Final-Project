from . import views
from django.urls import path, include
from django.contrib import admin

app_name = 'animes'
urlpatterns = [
    # TODO: Has to combine user log-in index field into the default anime listing page
    path('', views.IndexView.as_view(), name = 'index'),
    path('recommendation/<int:user_id>/', views.recommendation, name = 'recommendtaion'),
    path('stat/<int:user_id>/', views.stat, name = 'stat'),
    path('profile/<int:user_id>/', views.profile, name = 'profile'),
    path('<int:anime_id>/', views.review_detail, name = 'detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name = 'results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
    path('sign_up/', views.sign_up, name = "sign_up"),
    path('rank_by_date/', views.rank_by_date, name = "rank_by_date"),
    path('rank_by_name/', views.rank_by_name, name = "rank_by_name"),
    path('rank_by_rating/', views.rank_by_rating, name = "rank_by_rating"),
    path('search/', views.search, name="search"),
]
