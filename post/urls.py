from django.contrib.auth import login
from django.urls import path
from django.urls.resolvers import URLPattern

from post.forms import PostModelForm, Signin
from .views import AddCategory, AddPost, AddTag, DeleteCategory, DeletePost, DeleteTag, EditCategory, EditTag, SearchResultsView, TagDetailView, TagListView, login_user, myRegister,EditPost

from .views import CategoryDetailView, PostDetailView,PostListView,CategoryListView

urlpatterns = [
    path('<slug:slug>',PostDetailView.as_view(), name='post_detail'),
    path('', PostListView, name='post_list'),
    path('categories/',CategoryListView, name='category_list'),
    path('categories/<slug:slug>',CategoryDetailView, name='category_detail'),
    path('register/', myRegister ,name="register"),
    path('login/', login_user ,name="login"),
    path('create_post/', AddPost, name="post_form"),
    path('edit-post/<slug:slug>',EditPost,name="edit-post-form"),
    path('delete-post/<slug:slug>',DeletePost,name="delete-post"),
    path('edit-category/<slug:slug>',EditCategory,name="edit-category-form"),
    path('delete-category/<slug:slug>',DeleteCategory,name="delete-category"),
    path('create_category/', AddCategory, name="category_form"),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('edit-tag/<int:id>',EditTag,name="edit-tag-form"),
    path('delete-tag/<int:id>',DeleteTag,name="delete-tag"),
    path('create_tag/', AddTag, name="tag_form"),
    path('tags/',TagListView, name='tag_list'),
    path('tags/<int:id>',TagDetailView, name='tag_detail'),
]
