from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class BlogModel(models.Model):
    title = models.CharField(max_length=255)
    choices = (
        ("Web Development", "Web Development"),
        ("Mobile App Development", "Mobile App Development"),
        ("Data Science", "Data Science"),
        ("Cybersecurity", "Cybersecurity"),
        ("Blockchain", "Blockchain"),
    )
    content_type = models.CharField(max_length=255,choices=choices)
    content = models.TextField()
    banner_image = models.ImageField(upload_to="blog_banners/", null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author.username}-{self.title}"

#IMAGESS
class BlogImagesModel(models.Model):
    blog=models.ForeignKey(BlogModel,on_delete=models.CASCADE,related_name="images")
    images=models.ImageField(upload_to='blog_images/')
     
    def __str__(self):
        return f"Images for {self.blog.title}"


class CommentModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    blogs=models.ForeignKey(BlogModel,on_delete=models.CASCADE)
    textcontent=models.CharField(max_length=500)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f" {self.user.username} - {self.textcontent[:40]}"