from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse

from .models import Movie, MovieCrew, MovieComment, MovieRate
from .forms import MovieCommentForm, MovieRateForm


def index(request):
    return HttpResponse("Hello, World. You're here")


def movies_list(request):
    movie_list = Movie.objects.all().order_by('-release_date')[:10]
    contex = {
        'm_list': movie_list
    }
    return render(request, 'movies/list.html', contex)


def movies_detail(request, movie_id, comment_form=None, rate_form=None):
    movie = get_object_or_404(Movie, pk=movie_id)
    if comment_form is None:
        comment_form = MovieCommentForm()
    if rate_form is None:
        rate_form = MovieRateForm()
    context = {
        'movie': movie,
        'mc_list': MovieCrew.objects.select_related('crew', 'role').filter(movie=movie),
        'comment_list': MovieComment.objects.select_related('user').filter(
            movie=movie,
            status=MovieComment.APPROVED
        ).order_by('-id'),
        'rate_form': rate_form,
        'comment_form': comment_form,
        # 'rate_choice': range(1, 6),
    }
    return render(request, 'movies/detail.html', context)


def movies_comment(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    mcf = MovieCommentForm(request.POST)
    if not mcf.is_valid():
        return movies_detail(request, movie_id, comment_form=mcf)
    mc = mcf.save(commit=False)
    mc.user = request.user
    mc.movie = movie
    mc.save()
    return redirect('movie-detail', movie_id=movie_id)


def movies_rating(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    mrf = MovieRateForm(request.POST)
    if not mrf.is_valid():
        return movies_detail(request, movie_id, rate_form=mrf)
    mc = mrf.save(commit=False)
    mc.user = request.user
    mc.movie = movie
    mc.save()
    return redirect('movie-detail', movie_id=movie_id)
