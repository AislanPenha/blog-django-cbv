
from django.shortcuts import render
from django.core.paginator import Paginator
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404

PER_PAGE = 9

def index(request):
    # posts = Post.objects \
    #     .filter(is_published=True) \
    #     .order_by('-pk')
    posts = Post.objects.get_published()
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'page_title': 'Home - ',
    }
    return render(
        request,
        'blog/pages/index.html',
        context
    )


def created_by(request, author_id):
    # posts = Post.objects \
    #     .filter(is_published=True) \
    #     .order_by('-pk')
    user = User.objects.filter(pk=author_id).first()

    if user is None:
        raise Http404()
    
    posts = Post.objects.get_published() \
        .filter(created_by__pk=author_id)
    
    user_fullname = user.username

    if user.first_name:
        user_fullname = f'{user.first_name} {user.last_name}'
    
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    page_title = f'Pots de {user_fullname} - '

    context = {
        'page_obj': page_obj,
        'page_title': page_title
    }

    return render(
        request,
        'blog/pages/index.html',
        context
    )


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


        
