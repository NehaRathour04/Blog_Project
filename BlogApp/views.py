from django.shortcuts import render
from .models import BlogModel
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

# from .serializers import BlogSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import CommentModel
from .forms import BlogCreateForm
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.shortcuts import redirect
from .forms import RegisterForm


# fetch all blog model data
class BlogsView(APIView):
    def get(self, request):
        queries = BlogModel.objects.all().order_by("-created_at")
        return render(request, "index.html", {"posts": queries})


# single blog and its  comments based on pk
class BlogRetrieveView(APIView):
    def get(self, request, post_id):
        blog = get_object_or_404(BlogModel, pk=post_id)
        images = blog.images.all()

        comments = CommentModel.objects.filter(blogs=blog).order_by("-created_at")
        return render(
            request, "Blog.html", {"blog": blog, "images": images, "comments": comments}
        )


# add comments
class CommentsView(APIView):
    def post(self, request, post_id):
        user = request.user
        # print(user)
        blog = get_object_or_404(BlogModel, pk=post_id)
        # print(blog)
        comment = request.POST.get("content")
        # print(comment)
        CommentModel.objects.create(user=request.user, blogs=blog, textcontent=comment)
        return redirect("Blog", post_id=post_id)


# search
class SearchView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get("query")
        matching_queries = BlogModel.objects.filter(
            Q(title__icontains=query)
            | Q(content_type__icontains=query)
            | Q(content__icontains=query)
            | Q(author__username__icontains=query)
        )
        return render(request, "index.html", {"posts": matching_queries})


# filter
class FilterView(APIView):
    def get(self, request, q):
        if q == "All":
            matching_queries = BlogModel.objects.all()
        else:
            matching_queries = BlogModel.objects.filter(content_type__iexact=q)
        print(matching_queries)
        return render(request, "index.html", {"posts": matching_queries, "category": q})


# register
class RegisterView(APIView):
    def get(self, request):
        form = RegisterForm()
        return render(request, "Register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        # print(form,">>form")
        if form.is_valid():
            user = form.save(commit=False)
            # print(user,">>>>username")
            # hashing of the password
            user.set_password(form.cleaned_data["password"])
            print(user, "______________user_______")
            user.save()
            # token =Token.objects.create(user=user)
            # print(token)
            return redirect("login")
        else:
            return render(request, "Register.html", {"form": form})


from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from .forms import LoginForm


# get username or email
def get_user(username):
    try:
        user = User.objects.filter(Q(username=username) | Q(email=username)).first()
        if user:
            return [True, user]
        else:
            return [False, None]
    except:
        return [False, None]


# login
class LoginView(APIView):
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user_found, user = get_user(username)
            if user_found:
                user_data = authenticate(username=user.username, password=password)
                if user_data:
                    login(request, user_data)
                    token, _ = Token.objects.get_or_create(user=user)
                    return redirect("home")

                else:
                    return render(
                        request,
                        "index.html",
                        {"form": form, "error": "Invalid Credentials "},
                    )

            else:
                return render(
                    request,
                    "login.html",
                    {"form": form, "error": "Invalid Credentials "},
                )


# logout
class LogoutView(APIView):
    def get(self, request):
        logout(request)
        return redirect("home")


class UserSpecificBlogs(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        print("user : ", user)
        query = BlogModel.objects.filter(author=request.user).order_by("-created_at")
        print(query)
        return render(request, "user_profile.html", {"query": query})


from django.views import View
from .models import BlogImagesModel
from .forms import BlogImagesForm


class CreateBlogView(View):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        blog_form = BlogCreateForm()
        image_form = BlogImagesForm()
        return render(
            request,
            "BlogCreate_Edit.html",
            {"form": blog_form, "ImageForm": image_form, "operation": "Create"},
        )

    def post(self, request):
        blog_form = BlogCreateForm(request.POST, request.FILES)
        image_form = BlogImagesForm(request.POST, request.FILES)
        # print(request.FILES)
        if blog_form.is_valid() and image_form.is_valid():
            blog = blog_form.save(commit=False)
            blog.author = request.user
            blog.save()
            # print("FILES:", request.FILES)

            for img in request.FILES.getlist("images")[:3]:
                BlogImagesModel.objects.create(blog=blog, images=img)

            return redirect("UserBlogs")

        return render(
            request,
            "BlogCreate_Edit.html",
            {"form": blog_form, "ImageForm": image_form, "operation": "Create"},
        )


class EditBlogView(View):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        blog = get_object_or_404(BlogModel, pk=post_id, author=request.user)
        blog_form = BlogCreateForm(instance=blog)
        image_form = BlogImagesForm()
        return render(
            request,
            "BlogCreate_Edit.html",
            {
                "form": blog_form,
                "ImageForm": image_form,
                "operation": "Edit",
                "blog": blog,
            },
        )

    def post(self, request, post_id):
        blog = get_object_or_404(BlogModel, pk=post_id, author=request.user)
        blog_form = BlogCreateForm(request.POST, request.FILES, instance=blog)
        image_form = BlogImagesForm(request.POST, request.FILES)

        if blog_form.is_valid() and image_form.is_valid():
            blog = blog_form.save(commit=False)
            blog.author = request.user
            blog.save()
            # deletion
            images_to_delete = request.POST.getlist("delete_images")
            if images_to_delete:
                BlogImagesModel.objects.filter(
                    id__in=images_to_delete, blog=blog
                ).delete()

            existing_count = blog.images.count()  # images after deletion
            allowed_new = max(0, 3 - existing_count)  # slots left

            for img in request.FILES.getlist("images")[:allowed_new]:
                BlogImagesModel.objects.create(blog=blog, images=img)
            return redirect("UserBlogs")
        return render(
            request,
            "BlogCreate_Edit.html",
            {
                "form": blog_form,
                "ImageForm": image_form,
                "operation": "Edit",
                "blog": blog,
            },
        )


# delete
class DeleteBlogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        post = get_object_or_404(BlogModel, id=post_id)
        if post.author != request.user:
            return redirect("home")
        post.delete()
        return redirect("home")


class DeleteCommentView(APIView):
    def get(self, request, comment_id):
        comment = get_object_or_404(CommentModel, id=comment_id)
        blog_id = comment.blogs.id
        comment.delete()
        return redirect("Blog", post_id=blog_id)


class EditCommentView(APIView):
    def post(self, request, comment_id):
        comment = get_object_or_404(CommentModel,pk=comment_id,user=request.user)
        content=request.POST.get("content").strip()
        if content :
            comment.textcontent =content
            comment.save()
        return redirect("Blog",post_id=comment.blogs.id)


"""
class BlogModelCreate(APIView):
    def post(self, request):
        author = User.objects.get(username="NehaRathour")
        try:
            # Convert each dict in data into a BlogModel instance.
            query = request.data
            posts = []
            for item in query:
                posts.append(
                    BlogModel(
                        title=item.get("title"),
                        content=item.get("content"),
                        content_type=item.get("content_type"),
                        author=author,
                    )
                )
            # list of dictionary (instance model)
            BlogModel.objects.bulk_create(posts)
            return Response(
                {"message": f"{len(posts)} entries created"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
"""
