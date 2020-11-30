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
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

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
    return render(request, 'animes/index.html', context)


def rank_by_date(request):
    context = {}
    all_animes = AnimeWork.objects.all().order_by('anime_airing_start_date')[:60]
    paginator = Paginator(all_animes, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['object_list'] = page_obj
    context['page_obj'] = page_obj
    return render(request, 'animes/index.html', context)

def rank_by_rating(request):
    context = {}
    all_animes = AnimeWork.objects.all().order_by('-anime_rating')[:60]
    paginator = Paginator(all_animes, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['object_list'] = page_obj
    context['page_obj'] = page_obj
    return render(request, 'animes/index.html', context)

def rank_by_name(request):
    context = {}
    all_animes = AnimeWork.objects.all().order_by('anime_name')[:60]
    paginator = Paginator(all_animes, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['object_list'] = page_obj
    context['page_obj'] = page_obj
    return render(request, 'animes/index.html', context)

def recommendation(request, user_id):
    pass

def stat(request, user_id):
    pass

def profile(request, user_id):
    pass

class IndexView(generic.ListView):
    template_name = 'animes/index.html'
    model = AnimeWork
    paginate_by = 16
    # context_object_name = 'latest_question_list'

    def get_queryset(self):
        # print(AnimeWork.objects.all()[:30])
        return AnimeWork.objects.all()[:60]

class DetailView(generic.DetailView):
    model = AnimeWork
    template_name = 'animes/detail.html'

class AnimeWorkView(generic.DetailView):
    model = AnimeWork
    template_name = 'animes/detail.html'

class UserView(generic.DetailView):
    model = User
    template_name = 'animes/user.html'

def review_detail(request, anime_id):
    template_name = 'animes/detail.html'
    anime_work = get_object_or_404(AnimeWork, pk = anime_id)
    reviews = anime_work.review_set.all()
    new_review = None

    if request.method == 'POST':
        review_form = ReviewForm(data = request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit = False)
            new_review.review_anime_id = anime_work
            new_review.save()
    else:
        review_form = ReviewForm()
    return render(request, template_name, {
    'animework' : anime_work, 'reviews' : reviews, 'new_review' : new_review, 'review_form' : review_form
    })

def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'animes/detail.html', {
            'question' : question,
            'error_message' : "You didn't select a choice"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('animes:results', args=(question.id,)))

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request , 'animes/results.html', {'question' : question})
