# Generated by Django 4.0.2 on 2022-05-17 09:51

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0011_remove_user_per_group_user_user_per_group_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('whishlist', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=512), size=None)),
                ('voted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('voted_for', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.group_project')),
            ],
        ),
    ]