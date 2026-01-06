# from rest_framework import serializers
# from .models import BlogModel
# from django.contrib.auth.models import User

# class BlogSerializer(serializers.ModelSerializer) :
#     author = serializers.CharField(source="author.username", read_only=True)
#     class Meta :
#         model=BlogModel
#         fields=["id","title","content","content_type","author"]