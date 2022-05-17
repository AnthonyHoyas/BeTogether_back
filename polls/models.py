
from operator import mod
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


class Poll(models.Model):
    question = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)

    def __str__(self):
        return self.choice_text

class Group_project(models.Model):
    name = models.CharField(max_length=128)
    final_deadline = models.DateField()

    def __str__(self):
        return self.name

class Vote(models.Model):
    choice = models.ForeignKey(Choice, related_name='votes', on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    voted_by = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        unique_together = ("poll", "voted_by")

class Learner_project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    description = models.TextField
    database_schema_picture = models.ImageField(upload_to="images", blank=True, null=True)
    mockup_picture = models.ImageField(upload_to="images", blank=True, null=True)
    group_project = models.ForeignKey(Group_project, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Groups(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    group_project = models.ForeignKey(Group_project, on_delete=models.CASCADE)
    learner_project = models.OneToOneField(Learner_project, on_delete=models.CASCADE)
    # user = models.ManyToManyField(User, through='User_per_group', related_name='+')

    def __str__(self):
        return self.name

class User_per_group(models.Model):
    groups = models.ForeignKey(Groups, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ManyToManyField(User)

class Vote_list(models.Model):
    whishlist = ArrayField(
       models.CharField(max_length=512)
   )
    voted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    asigned_to = models.ForeignKey(Group_project, on_delete=models.CASCADE, blank=True, null=True )