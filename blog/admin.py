from django.contrib import admin

# Register your models here.
from .models import Post, PostImage, Adventurer, Rate

admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(Adventurer)
admin.site.register(Rate)
