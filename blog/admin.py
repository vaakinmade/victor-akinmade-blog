from django.contrib import admin
from .models import Post
from .models import Mail

admin.site.register(Post)
admin.site.register(Mail)