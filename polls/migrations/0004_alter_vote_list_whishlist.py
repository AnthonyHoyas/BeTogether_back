# Generated by Django 4.0.2 on 2022-05-18 12:23

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_promotion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote_list',
            name='whishlist',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=512, null=True), size=None),
        ),
    ]
