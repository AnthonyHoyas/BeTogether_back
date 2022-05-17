# Generated by Django 4.0.2 on 2022-05-17 07:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0003_group_project_groups_user_per_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='groups',
            name='user',
            field=models.ManyToManyField(related_name='+', through='polls.User_per_group', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='learner_project',
            name='group_project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.group_project'),
        ),
        migrations.AlterField(
            model_name='groups',
            name='learner_project',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='polls.learner_project'),
        ),
    ]