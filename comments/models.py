from django.db import models
from django.conf import settings


class Comment(models.Model):
    NEW = 0
    APPROVED = 1
    REJECTED = 2

    STATUS_CHOICES = (
        (NEW, 'new comment'),
        (APPROVED, 'approved'),
        (REJECTED, 'rejected'),
    )

    created_time = models.DateTimeField('created time', auto_now_add=True)
    updated_time = models.DateTimeField('updated time', auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='user_comments', editable=False)
    comment_text = models.TextField()
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=NEW, editable=False)
    moderated_time = models.DateTimeField('moderated time', null=True, blank=True)
    moderated_operator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='moderated_comments', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.user.is_staff:
            self.moderated_operator = self.user
        super(Comment, self).save(*args, **kwargs)
