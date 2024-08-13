from django.db import models
from django.contrib.auth.models import User
from main.models import Blog
import uuid

# Create your models here.
class BaseModel(models.Model):
    uid=models.UUIDField(default=uuid.uuid4, editable=False, unique=True,primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        
class Comment(BaseModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()

    def __str__(self):
        return f'Comment by {self.user.username} on {self.blog.title}'