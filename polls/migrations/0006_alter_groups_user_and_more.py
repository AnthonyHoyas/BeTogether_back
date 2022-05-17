# Generated by Django 4.0.2 on 2022-05-17 08:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0005_groups_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groups',
            name='user',
            field=models.ManyToManyField(related_name='+', through='polls.User_per_group', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='learner_project',
            name='group_project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.group_project'),
        ),
        migrations.RemoveField(
            model_name='user_per_group',
            name='user',
        ),
        migrations.AddField(
            model_name='user_per_group',
            name='user',
            field=models.ManyToManyField(related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]
