# Generated by Django 4.0.2 on 2022-05-30 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_alter_vote_list_asigned_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote_list',
            name='group_project_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.group_project'),
        ),
    ]
