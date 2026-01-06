from django.contrib import admin
from .models import BlogModel,CommentModel,BlogImagesModel
# Register your models here.
admin.site.register(BlogModel)
admin.site.register(BlogImagesModel)
admin.site.register(CommentModel)