# https://docs.djangoproject.com/pt-br/4.2/ref/class-based-views/
# Function Based Views -> São funções
# Class Based Views -> São classes (POO)

from typing import Any

from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Page, Tag
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404, HttpRequest
from django.views.generic import ListView, DetailView

PER_PAGE = 9

class PostListView(ListView):
    # Esses 2 foram tirados, por causa do queryset + get_published
    # model = Post
    # ordering = '-pk',
    template_name = 'blog/pages/index.html'
    # Tem que mudar essa variável que já é utilizada pelo Paginator page_obj => posts
    # object_list == posts
    context_object_name = 'posts' 
    
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published() # faz o método abaixo
    # Se quiser sobrescrever a queryset
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(is_published=True)
    #     return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'page_title': 'Home - '
        })
        # print(context)
        # context = {
        #     'paginator': <django.core.paginator.Paginator object at 0x77e31c3d8050>, 
        #     'page_obj': <Page 1 of 2>, 
        #     'is_paginated': True, 
        #     'object_list': <QuerySet [
        #         <Post: Globo dobra tempo do pré-jogo>, 
        #         <Post: Globo dobra tempo do pré-jogo>, 
        #     ]>, 
        #     'posts': <QuerySet [
        #         <Post: Globo dobra tempo do pré-jogo>, 
        #         <Post: Globo dobra tempo do pré-jogo>, 
        #     ]>, 
        #     'view': <blog.views.views.PostListView object at 0x77e31c3d7fb0>, 
        #     'page_title': 'Home - '
        # }

        return context

class CreatedByListView(PostListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}

    # Ordem de processamento
    def setup(self, request, *args, **kwargs):
        print('Este é o método setup')
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        print('Este é o método dispatch')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        print('Este é o método get')
        author_id = self.kwargs.get('author_id')
        user = User.objects.filter(pk=author_id).first()

        if user is None:
            raise Http404() # return redirect('blog:index')
        
        self._temp_context.update({
            'author_id': author_id,
            'user': user
        })
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        print('Este é o método get_queryset')
        qs = super().get_queryset()
        qs = qs.filter(created_by__pk=self._temp_context['user'].pk)
        return qs
    
    def get_context_data(self, **kwargs):
        print('Este é o método get_context_data')

        context =  super().get_context_data(**kwargs)

        # author_id = self.kwargs.get('author_id')
        # user = User.objects.filter(pk=author_id).first()

        # if user is None:
        #     raise Http404()
        
        user = self._temp_context['user']
        user_fullname = user.username

        if user.first_name:
            user_fullname = f'{user.first_name} {user.last_name}'
        
        page_title = f'Pots de {user_fullname} - '

        context.update({
            'page_title': page_title
        })
        return context
    
    def get_context_object_name(self, object_list):
        print('Este é o método get_context_object_name')
        return super().get_context_object_name(object_list)
    
    def render_to_response(self, context, **response_kwargs):
        print('Este é o método render_to_response')
        return super().render_to_response(context, **response_kwargs)
    
    def get_template_names(self):
        print('Este é o método get_template_names')
        return super().get_template_names()
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        print('Este é o método http_method_not_allowed')
        return super().http_method_not_allowed(request, *args, **kwargs)
    
    
class CategoryListView(PostListView):
    def get_queryset(self):
        self.allow_empty = False # Levanta um erro 404, se estiver vazio
        qs = super().get_queryset()
        return qs.filter(category__slug=self.kwargs.get('category_slug'))
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        object_list = context['object_list']
        page_title = f'Categoria: {object_list[0].category.name} - '

        context.update({
            'page_title': page_title
        })
        return context
    
    
class TagListView(PostListView):
    def get_queryset(self):
        self.allow_empty = False # Levanta um erro 404, se estiver vazio
        qs = super().get_queryset()
        return qs.filter(tags__slug=self.kwargs.get('tag_slug'))

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        tag = get_object_or_404(
            Tag,
            slug=self.kwargs.get('tag_slug')
        )
  
        page_title = f'Tag: {tag.name} - '
        context.update({
            'page_title': page_title
        })
        return context


class SearchListView(PostListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._search_value = ''

    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get('search', '').strip()
        print(self._search_value)
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        search_value = self._search_value
        qs = super().get_queryset()
        return qs.filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
        )[:PER_PAGE]
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        search_value = self._search_value
        page_title = f'Search: {search_value[:20]} - '
        context.update({
            'search_value': search_value,
            'page_title': page_title,
        })
        return context
    
    def get(self, request, *args, **kwargs):
        if self._search_value == '':
            return redirect('blog:index')
        return super().get(request, *args, **kwargs)


class PageDetailView(DetailView):
    model = Page
    template_name = 'blog/pages/page.html'
    slug_field = 'slug'
    slug_url_kwarg = 'page_slug'
    context_object_name = 'page'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        page = context['page']
        page_title = f'Página: {page.title} - '
        context.update({
            'page_title': page_title,
        })
        return context
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_published=True)


class PostDetailView(DetailView):
    template_name = 'blog/pages/post.html'
    slug_field = 'slug'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    queryset = Post.objects.get_published()

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        post = context['post']
        page_title = f'Post: {post.title} - '
        context.update({
            'page_title': page_title,
        })
        return context