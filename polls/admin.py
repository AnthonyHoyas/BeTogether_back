from django.contrib import admin

# Register your models here.
from .models import Group_project, Groups, Learner_project, Poll, Choice, User_per_group

admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(Learner_project)
admin.site.register(Group_project)
admin.site.register(Groups)
admin.site.register(User_per_group)
