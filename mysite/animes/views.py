from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.core.paginator import Paginator


from .models import AnimeWork, User, Tag, ProductionCompany, Review
from .forms import ReviewForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from collections import Counter, defaultdict
import json
import numpy as np

# @login_required
# def index(request):
#     return render(request, 'animes/index.html')

def sign_up(request):
    context = {}
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, 'animes/index.html')
    context['form'] = form
    return render(request, 'animes/sign_up.html', context)

def search(request):
    context = {}
    keyword = request.GET['keyword']
    selected_animes = AnimeWork.objects.filter(anime_name__icontains=keyword)
    paginator = Paginator(selected_animes, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['object_list'] = page_obj
    context['page_obj'] = page_obj
    context['tags'] = Tag.objects.all()
    return render(request, 'animes/index.html', context)

def search_by_tag(request):
    context = {}
    tag_info = request.GET['tag_info']
    selected_animes = AnimeWork.objects.filter(tag__tag_name__contains=tag_info)
    paginator = Paginator(selected_animes, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['object_list'] = page_obj
    context['page_obj'] = page_obj
    context['tags'] = Tag.objects.all()
    return render(request, 'animes/index.html', context)

def rank_by_date(request):
    context = {}
    all_animes = AnimeWork.objects.all().order_by('anime_airing_start_date')[:60]
    paginator = Paginator(all_animes, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['object_list'] = page_obj
    context['page_obj'] = page_obj
    context['tags'] = Tag.objects.all()
    return render(request, 'animes/index.html', context)

def rank_by_rating(request):
    context = {}
    all_animes = AnimeWork.objects.all().order_by('-anime_rating')[:60]
    paginator = Paginator(all_animes, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['object_list'] = page_obj
    context['page_obj'] = page_obj
    context['tags'] = Tag.objects.all()
    return render(request, 'animes/index.html', context)

def rank_by_name(request):
    context = {}
    all_animes = AnimeWork.objects.all().order_by('anime_name')[:60]
    paginator = Paginator(all_animes, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['object_list'] = page_obj
    context['page_obj'] = page_obj
    context['tags'] = Tag.objects.all()
    return render(request, 'animes/index.html', context)

@login_required
def recommendation(request):
    context = {}
    user = request.user
    anime_watch_list = [e.anime_name for e in user.watchlist.anime_works.all()]
    anime_wish_list = [e.anime_name for e in user.watchlist.anime_works.all()]
    recommendation = None
    # If the user does not have any previous watching history, recommend him/her
    # the top 10 animes with the hightest rating
    if len(anime_watch_list) == 0 and len(anime_wish_list) == 0:
        recommendation = AnimeWork.objects.all().order_by('anime_rating')[:10]
        context['recommendation'] = recommendation
        return render(request, 'animes/recommendation.html', context)
    wish_tag = Counter()
    watch_tag = Counter()
    tag_score = defaultdict(int)
    for anime in anime_wish_list:
        wish_tag.update([t.tag_name for t in Tag.objects.filter(tag_anime_works__anime_name__icontains=anime)])
    for anime in anime_watch_list:
        watch_tag.update([t.tag_name for t in Tag.objects.filter(tag_anime_works__anime_name__icontains=anime)])
    wish_tag = dict(wish_tag)
    watch_tag = dict(watch_tag)
    for tag in wish_tag.keys():
        tag_score[tag] += wish_tag[tag] * 2
    for tag in watch_tag.keys():
        tag_score[tag] += watch_tag[tag]
    # sample two categories of animes based on the weighted tag score
    tags = list(tag_score.keys())
    normalization_const = sum([v for k, v in tag_score.items()])
    probs = []
    for t in tags:
        probs.append(tag_score[t] * 1.0 / normalization_const)
    recommended_tags = np.random.choice(tags, 2, p = probs).tolist()

    recommendation = AnimeWork.objects.exclude(anime_name__in=anime_watch_list).exclude(anime_name__in=anime_wish_list) \
    .filter(tag__tag_name__in=recommended_tags).order_by('-anime_rating')[:5]
    context['recommendation'] = recommendation

    return render(request, 'animes/recommendation.html', context)

@login_required
def stat(request):
    context = {}
    user = request.user
    # user_2 = User.objects.get(username='Kai')
    # print('user_2', user_2.__dict__)
    # print('watch_list', user_2.watchlist)
    # print('user', user.__dict__)
    wish_list_anime = [e.anime_name for e in user.wishlist.anime_works.all()]
    watch_list_anime = [e.anime_name for e in user.watchlist.anime_works.all()]
    wish_tag = Counter()
    watch_tag = Counter()
    wish_company = Counter()
    watch_company = Counter()
    for anime in wish_list_anime:
        wish_tag.update([t.tag_name for t in Tag.objects.filter(tag_anime_works__anime_name__icontains=anime)])
        wish_company.update([c.company_name for c in ProductionCompany.objects.filter(company_anime_works__anime_name__icontains=anime)])
    for anime in watch_list_anime:
        watch_tag.update([t.tag_name for t in Tag.objects.filter(tag_anime_works__anime_name__icontains=anime)])
        watch_company.update([c.company_name for c in ProductionCompany.objects.filter(company_anime_works__anime_name__icontains=anime)])
    json_wish_tag = json.dumps([{'tag_name' : key, 'count' : value} for key, value in wish_tag.items()])
    json_watch_tag = json.dumps([{'tag_name' : key, 'count' : value} for key, value in watch_tag.items()])
    context['json_wish_tag'] = json_wish_tag
    context['json_watch_tag'] = json_watch_tag
    json_wish_company = json.dumps([{'company_name' : key, 'count' : value} for key, value in wish_company.items()])
    json_watch_company = json.dumps([{'company_name' : key, 'count' : value} for key, value in watch_company.items()])
    context['json_wish_company'] = json_wish_company
    context['json_watch_company'] = json_watch_company
    # print('json', json_watch_company)
    return render(request, 'animes/stat.html', context)

@login_required
def profile(request):
    return render(request, 'animes/profile.html')

class IndexView(generic.ListView):
    template_name = 'animes/index.html'
    model = AnimeWork
    paginate_by = 16
    # context_object_name = 'latest_question_list'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['tags'] = Tag.objects.all()
        return context

    def get_queryset(self):
        # print(AnimeWork.objects.all()[:30])
        return AnimeWork.objects.all()

class DetailView(generic.DetailView):
    model = AnimeWork
    template_name = 'animes/detail.html'

class AnimeWorkView(generic.DetailView):
    model = AnimeWork
    template_name = 'animes/detail.html'

class UserView(generic.DetailView):
    model = User
    template_name = 'animes/user.html'

@login_required
def review_detail(request, anime_id):
    template_name = 'animes/detail.html'
    anime_work = get_object_or_404(AnimeWork, pk = anime_id)
    reviews = anime_work.review_set.all()
    user = request.user
    new_review = None

    if request.method == 'POST':
        review_form = ReviewForm(data = request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit = False)
            new_review.review_anime_id = anime_work
            new_review.reviewer_id = user
            new_review.save()
    else:
        review_form = ReviewForm()
    return render(request, template_name, {
    'animework' : anime_work, 'reviews' : reviews, 'new_review' : new_review, 'review_form' : review_form
    })
