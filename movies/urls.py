from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.movies_list, name='movie-list'),
    path('<int:movie_id>/', views.movies_detail, name='movie-detail'),
    path('<int:movie_id>/post_comment/', views.movies_comment, name='movie-post-comment'),
    path('<int:movie_id>/post_rating/', views.movies_rating, name='movie-post-rating'),
]
