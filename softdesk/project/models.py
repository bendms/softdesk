from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# from authentication.models import CustomUser, Contributor

# Create your models here.

# class Project(models.Model):
#     # user_id = models.IntegerField()
#     title = models.CharField(max_length=128)
#     description = models.CharField(max_length=8192)
#     type = models.CharField(max_length=128)
#     author_user_id = models.ForeignKey(
#         to=User,
#         on_delete=models.CASCADE,
#         related_name='author_user_id'
#     )
    
#     def __str__(self):
#         return self.title



class Project(models.Model):
    # user_id = models.IntegerField()
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=8192)
    type = models.CharField(max_length=128)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

class Issue(models.Model):
    # project_id = models.IntegerField()
    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=8192)
    tag = models.CharField(max_length=128)
    priority = models.CharField(max_length=128)
    project_id = models.IntegerField()
    status = models.CharField(max_length=128)
    author_user_id = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='author_user_id'
    )
    assigned_user_id = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='assigned_user_id'
    )
    created_time = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    # comment_id = models.IntegerField()
    description = models.CharField(max_length=8192)
    author_user_id = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )
    issue_id = models.ForeignKey(
        to=Issue,
        on_delete=models.CASCADE
    )
    created_time = models.DateTimeField(auto_now_add=True)
    

class Contributor(models.Model):

    # user = models.ForeignKey(
    #     to='User', on_delete=models.CASCADE, related_name='contributor'
    # )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    permission = models.CharField(max_length=128)
    role = models.CharField(max_length=128)
    
    class Meta:
        unique_together = ("user", "project")