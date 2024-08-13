from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class BaseModel(models.Model):
    uid=models.UUIDField(default=uuid.uuid4, editable=False, unique=True,primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Blog(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='blogs')
    title=models.CharField(max_length=50)
    content = models.TextField()
    image=models.ImageField(blank=True,null=True,upload_to='blog/image')

    def __str__(self):
        return self.title

