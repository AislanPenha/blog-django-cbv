from django.urls import path
from blog import views
from blog.views import PostListView, CreatedByListView, CategoryListView

app_name = 'blog'

urlpatterns = [
    path(
        '', 
        PostListView.as_view(), 
        name='index'
    ),
    path(
        'created_by/<int:author_id>/', 
        CreatedByListView.as_view(), 
        name='created_by'
    ),
    path(
        'category/<slug:category_slug>/', 
        CategoryListView.as_view(), 
        name='category'
    ),
    path('post/<slug:slug>/', views.post, name='post'),
    path('page/<slug:slug>/', views.page, name='page'),
    path('tag/<slug:tag_slug>/', views.tag, name='tag'),
    path('search/', views.search, name='search'),
]
