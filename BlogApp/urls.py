from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path("PostModelCreateApi", views.PostModelCreate.as_view(), name="PostModelCreateApi"),
    path("", views.BlogsView.as_view(), name="home"),
    path("Search", views.SearchView.as_view(), name="Search"),
    path("Filter/<str:q>/", views.FilterView.as_view(), name="Filter"),
    path("Blog/<int:post_id>", views.BlogRetrieveView.as_view(), name="Blog"),
    path("addcomment/<int:post_id>", views.CommentsView.as_view(), name="add_comment"),
    path("register", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("userBlogs", views.UserSpecificBlogs.as_view(), name="UserBlogs"),
    path("newBlog", views.CreateBlogView.as_view(), name="NewBlog"),
    path("editBlog/<int:post_id>", views.EditBlogView.as_view(), name="EditBlog"),
    path("deleteBlog/<int:post_id>/", views.DeleteBlogView.as_view(), name="DeleteBlog"),
    path("deleteComment/<int:comment_id>/",views.DeleteCommentView.as_view(),name="deleteComment" ),
    path( "editComment/<int:comment_id>/",  views.EditCommentView.as_view(),name="editComment" ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
