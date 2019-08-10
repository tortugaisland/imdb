from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator


class Rate(models.Model):
    created_time = models.DateTimeField('created time', auto_now_add=True)
    updated_time = models.DateTimeField('updated time', auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='user_ratings', editable=False)
    point = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)])



