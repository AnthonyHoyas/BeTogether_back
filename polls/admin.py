from django.contrib import admin

# Register your models here.
from .models import Learner_project, Poll, Choice

admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(Learner_project)
