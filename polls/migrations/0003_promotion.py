# Generated by Django 4.0.2 on 2022-05-17 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=128, null=True)),
            ],
        ),
    ]
