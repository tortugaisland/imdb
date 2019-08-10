from django.db import models
from django.conf import settings

from comments.models import Comment
from ratings.models import Rate


class Genre(models.Model):
    created_time = models.DateTimeField('created time', auto_now_add=True)
    title = models.CharField('title', max_length=150)

    def __str__(self):
        return self.title


class Crew(models.Model):
    MALE = 'm'
    FEMALE = 'f'

    GENDER_TYPES = (
        (MALE, 'male'),
        (FEMALE, 'female'),
    )

    created_time = models.DateTimeField('created time', auto_now_add=True)
    first_name = models.CharField('first name', max_length=100)
    last_name = models.CharField('last name', max_length=100)
    birth_date = models.DateField('birth date', null=True, blank=True)
    avatar = models.ImageField('avatar', blank=True)
    gender = models.CharField('Gender', max_length=1, choices=GENDER_TYPES)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Movie(models.Model):
    created_time = models.DateTimeField('created time', auto_now_add=True)
    updated_time = models.DateTimeField('updated time', auto_now=True)
    title = models.CharField('title', max_length=150)
    release_date = models.DateField('release date')
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT)
    is_enable = models.BooleanField('enabled?', default=True)
    crew_list = models.ManyToManyField('Crew', through='MovieCrew')
    picture = models.ImageField(blank=True)

    def __str__(self):
        # return "%s - %s" % (self.title, self.release_date)
        # return "%(title)s - %(r_date)s" % {'r_date': self.release_date, 'title': self.title}
        # return "{} - {}".format(self.title, self.release_date)
        # return "{title} - {r_date}".format(r_date=self.release_date, title=self.title)
        return f"{self.title} - {self.release_date}"

    def rating_avg(self):
        avg = self.rates.aggregate(movie_avg_rate=models.Avg('point'))
        return avg['movie_avg_rate'] or 0

    def rating_count(self):
        return self.rates.count()

    def get_picture(self):
        return self.picture.url if self.picture else f"{settings.STATIC_URL}movies/1.jpg"


class Role(models.Model):
    created_time = models.DateTimeField('created time', auto_now_add=True)
    title = models.CharField('title', max_length=150)
    slug = models.SlugField('slug', unique=True)

    def __str__(self):
        return self.title


class MovieCrew(models.Model):
    created_time = models.DateTimeField('created time', auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('movie', 'crew', 'role')

    def __str__(self):
        return f"{self.movie} - {self.crew} - {self.role}"


class MovieComment(Comment):
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE)


class MovieRate(Rate):
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE, related_name='rates')
