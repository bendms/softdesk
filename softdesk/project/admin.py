from django.contrib import admin
from .models import Project, Issue, Comment
from authentication.models import Contributor
# Register your models here.

admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Comment)
admin.site.register(Contributor)
