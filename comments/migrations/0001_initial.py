# Generated by Django 2.2.3 on 2019-08-03 11:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='updated time')),
                ('comment_text', models.TextField()),
                ('status', models.PositiveSmallIntegerField(choices=[('new comment', 0), ('approved', 1), ('rejected', 2)], default=0)),
                ('moderated_time', models.DateTimeField(null=True, verbose_name='moderated time')),
                ('moderated_operator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='moderated_comments', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
