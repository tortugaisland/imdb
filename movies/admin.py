from django.contrib import admin
from datetime import timedelta, datetime
from django.db.models import F


from .models import Movie, Genre, Crew, Role, MovieCrew, MovieComment


admin.site.register(Genre)
admin.site.register(Crew)
admin.site.register(Role)
admin.site.register(MovieCrew)


def make_enable(modeladmin, request, queryset):
    queryset.update(is_enable=True)
make_enable.short_description = "Mark selected items as enabled"


def make_disable(modeladmin, request, queryset):
    queryset.update(is_enable=False)
make_disable.short_description = "Mark selected items as disabled"


class MovieCrewInlineAdmin(admin.TabularInline):
    model = MovieCrew
    extra = 0
    raw_id_fields = ('crew', )

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'genre', 'is_enable', 'id', 'created_time')
    list_filter = ('is_enable', 'created_time', 'genre', )
    search_fields = ('title', )
    actions = [make_enable, make_disable, 'add_years']
    inlines = [MovieCrewInlineAdmin,]

    def add_years(self, request, queryset):
        # for obj in queryset:
        #     new_year = obj.release_date.year + 3
        #     obj.release_date = obj.release_date.replace(year=new_year)
        #     obj.save()
        queryset.update(release_date=F('release_date')+timedelta(days=3*365))
    add_years.short_description = "Add 3 years to selected items"


@admin.register(MovieComment)
class MovieCommentAdmin(admin.ModelAdmin):
    list_display = ('created_time', 'user', 'movie', 'status')
    list_filter = ('status', 'created_time')
    raw_id_fields = ('movie', 'user')
    actions = ['make_approved']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def make_approved(modeladmin, request, queryset):
        queryset.update(
            status=MovieComment.APPROVED,
            moderated_time=datetime.now(),
            moderated_operator=request.user
        )
    make_approved.short_description = "Mark selected items as approved"