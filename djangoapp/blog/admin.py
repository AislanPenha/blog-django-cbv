from django.contrib import admin
from blog.models import Tag, Category, Page, Post
from django_summernote.admin import SummernoteModelAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'slug',
    list_display_links = 'name', 
    search_fields = 'id', 'name', 'slug',
    list_per_page = 10
    ordering = '-id', 
    list_display = 'id', 'name', 'slug',
    prepopulated_fields = {
        'slug': ('name',),
    }

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'slug',
    list_display_links = 'name', 
    search_fields = 'id', 'name', 'slug',
    list_per_page = 10
    ordering = '-id', 
    list_display = 'id', 'name', 'slug',
    prepopulated_fields = {
        'slug': ('name',),
    }

@admin.register(Page)
class PageAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = 'id', 'title', 'slug', 'is_published',
    list_display_links = 'title', 
    search_fields = 'id', 'title', 'slug',
    list_editable = 'is_published',
    list_per_page = 10
    ordering = '-id', 
    prepopulated_fields = {
        'slug': ('title',),
    }

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = 'id', 'title', 'slug', 'is_published', \
        'category',
    list_display_links = 'title', 
    search_fields = 'id', 'title', 'slug', 'title', 'excerpt', 'content', 
    list_editable = 'is_published',
    list_per_page = 50
    list_filter = 'category', 'is_published',
    ordering = '-id', 
    prepopulated_fields = {
         'slug': ('title',),
    }
    readonly_fields = (
        'created_at', 'updated_at', 'created_by', 'updated_by', 'link'
    )
    autocomplete_fields = 'tags', 'category',

    def link(self, obj):
        if not obj.pk:
            return '-'
        
        # alink = reverse('blog:post', args=(obj.slug, ))
        alink = obj.get_absolute_url()
        
        ahref = f'<a href="{alink}" target="_blank"> Ver post</a> '
        return mark_safe(ahref) #mar_safe => informa ao django que pode fazer um link seguro
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user

        obj.save()