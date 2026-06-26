from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path(
        '', 
        views.PostListView.as_view(), 
        name='index'
    ),
    path(
        'created_by/<int:author_id>/', 
        views.CreatedByListView.as_view(), 
        name='created_by'
    ),
    path(
        'category/<slug:category_slug>/', 
        views.CategoryListView.as_view(), 
        name='category'
    ),
    path(
        'tag/<slug:tag_slug>/', 
        views.TagListView.as_view(), 
        name='tag'
    ),
    path(
        'search/', 
        views.SearchListView.as_view(), 
        name='search'
    ),
    path('post/<slug:slug>/', views.post, name='post'),
    path('page/<slug:slug>/', views.page, name='page'),
]
