from . import views
from django.urls import path, include
from django.contrib import admin

app_name = 'animes'
urlpatterns = [
    # TODO: Has to combine user log-in index field into the default anime listing page
    # path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name = 'detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name = 'results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
    path('', include('django.contrib.auth.urls')),
    path('', views.index, name = 'home'),
    path('sign_up/', views.sign_up, name = "sign_up")
]
