# https://docs.djangoproject.com/pt-br/4.2/ref/class-based-views/
# Function Based Views -> São funções
# Class Based Views -> São classes (POO)

from typing import Any

from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404, HttpRequest

from django.views.generic import ListView

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
    # def get_queryset(self):
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
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}

    # Ordem de processamento
    def setup(self, *args, **kwargs):
        print('Este é o método setup')
        return super().setup(*args, **kwargs)
    
    def dispatch(self, *args, **kwargs):
        print('Este é o método dispatch')
        return super().dispatch(*args, **kwargs)
    
    def get(self, *args, **kwargs):
        print('Este é o método get')
        author_id = self.kwargs.get('author_id')
        user = User.objects.filter(pk=author_id).first()

        if user is None:
            raise Http404() # return redirect('blog:index')
        
        self._temp_context.update({
            'author_id': author_id,
            'user': user
        })
        return super().get(*args, **kwargs)
    
    def get_queryset(self, *args, **kwargs):
        print('Este é o método get_queryset')
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(created_by__pk=self._temp_context['user'].pk)
        return qs
    
    def get_context_data(self, *args, **kwargs):
        print('Este é o método get_context_data')

        context =  super().get_context_data(*args, **kwargs)

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
    
    def get_context_object_name(self, *args, **kwargs):
        print('Este é o método get_context_object_name')
        return super().get_context_object_name(*args, **kwargs)
    
    def render_to_response(self, *args, **kwargs):
        print('Este é o método render_to_response')
        return super().render_to_response(*args, **kwargs)
    
    def get_template_names(self, *args, **kwargs):
        print('Este é o método get_template_names')
        return super().get_template_names(*args, **kwargs)
    
    def http_method_not_allowed(self, *args, **kwargs):
        print('Este é o método http_method_not_allowed')
        return super().http_method_not_allowed(*args, **kwargs)
    
    
class CategoryListView(PostListView):
    def get_queryset(self) -> QuerySet[Any]:
        self.allow_empty = False # Levanta um erro 404, se estiver vazio
        qs = super().get_queryset()
        return qs.filter(category__slug=self.kwargs.get('category_slug'))
    
    def get_context_data(self, *args, **kwargs):
        context =  super().get_context_data(*args, **kwargs)
        object_list = context['object_list']
        page_title = f'Categoria: {object_list[0].category.name} - '

        context.update({
            'page_title': page_title
        })
        return context
    
    
    

def category(request, category_slug):
    # posts = Post.objects \
    #     .filter(is_published=True) \
    #     .order_by('-pk')
    posts = Post.objects.get_published() \
        .filter(category__slug=category_slug)
    
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404()
    
    page_title = f'Categoria: {page_obj[0].category.name} - '
    context = {
        'page_obj': page_obj,
        'page_title': page_title
    }
    return render(
        request,
        'blog/pages/index.html',
        context
    )


def tag(request, tag_slug):
    # posts = Post.objects \
    #     .filter(is_published=True) \
    #     .order_by('-pk')
    posts = Post.objects.get_published() \
        .filter(tags__slug=tag_slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if len(page_obj) == 0:
        raise Http404()
    
    page_title = f'Tag: {page_obj[0].tags.first().name} - '
    context = {
        'page_obj': page_obj,
        'page_title': page_title
    }

    return render(
        request,
        'blog/pages/index.html',
        context
    )


def search(request):

    search_value = request.GET.get('search', '').strip()

    posts = Post.objects.get_published() \
        .filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
        )[:PER_PAGE]
    
    page_title = f'Search: {search_value[:20]} - '

    context = {
        'page_obj': posts,
        'search_value': search_value,
        'page_title': page_title,
    }
    return render(
        request,
        'blog/pages/index.html',
        context
    )


def page(request, slug):
    page_obj = Page.objects \
        .filter(is_published=True) \
        .filter(slug=slug).first()

    if page_obj is None:
        raise Http404()
    
    page_title = f'Página: {page_obj.title} - '

    context = {
        'page': page_obj,
        'page_title': page_title,
    }
    return render(
        request,
        'blog/pages/page.html',
        context
    )


def post(request, slug):
    post_obj = Post.objects.get_published() \
        .filter(slug=slug) \
        .first()
    
    if post_obj is None:
        raise Http404()
    
    page_title = f'Post: {post_obj.title} - '

    context = {
        'post': post_obj,
        'page_title': page_title,
    }

    return render(
        request,
        'blog/pages/post.html',
        context
    )


        
