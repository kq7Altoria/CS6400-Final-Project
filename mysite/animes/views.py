from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question, AnimeWork, User, Tag, ProductionCompany, Review
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, 'animes/index.html')

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


class IndexView(generic.ListView):
    template_name = 'animes/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """ Return the last five published questions. """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = AnimeWork
    template_name = 'animes/anime_detail.html'
    # def get_queryset(self):
    #     """
    #     Exludes any quesitons that aren't publised yet.
    #     """
    #     return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'animes/results.html'

# Create your views here.
# def index(request):a
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('animes/index.html')
#     context = {
#         'latest_question_list' : latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))
#
# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, 'animes/detail.html', {'question' : question})
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'animes/results.html', {'question' : question})

class AnimeWorkView(generic.DetailView):
    model = AnimeWork
    template_name = 'animes/anime_detail.html'

class UserView(generic.DetailView):
    model = User
    template_name = 'animes/user.html'


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
