from django.contrib import admin
from .models import Comment
# Register your models here.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=['uid','blog','user','content','created_at','updated_at']
    list_display_links=['uid','blog']
    raw_id_fields = ('blog',)