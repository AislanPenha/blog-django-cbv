from django.db import models
from django.contrib.auth.models import User
from utils.rands import slug_new
from utils.images import resize_image
from django_summernote.models import AbstractAttachment
from django.urls import reverse

class PostAttachment(AbstractAttachment):
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name
        
        current_file_name = str(self.file.name)
        super_save = super().save(*args, **kwargs)
        file_change = False

        if self.name:
            file_change = current_file_name != self.file.name
        if file_change:
            resize_image(self.file, 900)

        return super_save
    
class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=100)
    slug = models.SlugField(
        unique=True,
        default=None,
        null=True,
        blank=True,
        max_length=100
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slug_new(self.name)

        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f'{self.name}'
    
class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=100)
    slug = models.SlugField(
        unique=True,
        default=None,
        null=True,
        blank=True,
        max_length=100
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slug_new(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f'{self.name}'
    
class Page(models.Model):
    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    title = models.CharField(max_length=100)
    slug = models.SlugField(
        unique=True,
        default="",
        null=True,
        blank=True,
        max_length=100
    )
    is_published = models.BooleanField(
        default=False,
        help_text='Este campo precisará estar marcado para a página ser exibida publicamente.')
    content = models.TextField()

    def get_absolute_url(self):
        if not self.is_published:
            return reverse('blog:index')
        
        return reverse("blog:page", args=(self.slug, ))
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slug_new(self.title, 4)
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f'{self.title}'
    
class PostManager(models.Manager):
    def get_published(self):
        return self \
            .filter(is_published=True) \
            .order_by('-pk')

class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


    objects: PostManager = PostManager()   # Padrão objects = models.Manager() 
    title = models.CharField(max_length=100)
    slug = models.SlugField(
        unique=True,
        default="",
        null=True,
        blank=True,
        max_length=100
    )
    excerpt = models.CharField(max_length=150)
    is_published = models.BooleanField(
        default=False,
        help_text='Este campo precisará estar marcado para a post ser exibido publicamente.')
    content = models.TextField()
    cover = models.ImageField(upload_to='posts/%Y/%m/', blank=True, default='')
    cover_in_post_content = models.BooleanField(
        default=True,
        help_text='Exibe a image de capa também dentro do conteúdo do post.'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='post_created_by' # user.post_set.title | user.post_created_by.title
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='post_updated_by'  # user.post_set.title | user.post_updated_by.title
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        blank=True, default=None,
    )
    tags = models.ManyToManyField(Tag, blank=True, default='')

    def get_absolute_url(self):
        if not self.is_published:
            return reverse('blog:index')
        
        return reverse("blog:post", args=(self.slug, ))
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slug_new(self.title, 4)

        current_cover_name = str(self.cover.name)
        super_save = super().save(*args, **kwargs)
        cover_change = False
        if self.cover:
            cover_change = current_cover_name != self.cover.name
        if cover_change:
            resize_image(self.cover, 900)

        return super_save
    
    def __str__(self) -> str:
        return f'{self.title}'