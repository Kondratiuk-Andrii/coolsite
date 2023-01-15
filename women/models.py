from django.db import models
from django.db.models import Count
from django.urls import reverse

from pytils.translit import slugify


class Women(models.Model):
    title = models.CharField(max_length=255, verbose_name='Имя')
    slug = models.SlugField(max_length=255, blank=True, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name='Текст статьи')
    photo = models.ImageField(upload_to="photo/%Y/%m/%d/", verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=True, verbose_name='Статус публикации')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('women:post', kwargs={'post_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
            identity = len(Women.objects.annotate(Count('slug')).filter(slug__contains=self.slug))
            if identity:
                self.slug += str(identity + 1)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'
        ordering = ['id']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('women:category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']
