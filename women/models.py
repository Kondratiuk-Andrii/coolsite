from django.db import models
from django.urls import reverse
from pytils.translit import slugify
from django.utils.timezone import now


class Women(models.Model):
    title = models.CharField('Заголовок', max_length=255)
    slug = models.SlugField('URL', max_length=255, unique=True, db_index=True)
    content = models.TextField('Текст статьи', null=True, blank=True)
    photo = models.ImageField('Фото', upload_to='women_images/%Y/%m/%d/', null=True, blank=True)
    time_create = models.DateTimeField('Время создания', auto_now_add=True)
    time_update = models.DateTimeField('Время изменения', auto_now=True)
    is_published = models.BooleanField('Опубликовано', default=True)
    category = models.ForeignKey(
        to='Category',
        on_delete=models.PROTECT,
        related_name='women',
        verbose_name='Категория',
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('women:post_detail', kwargs={'post_slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if Women.objects.filter(slug__contains=self.slug).exists():
            self.slug += str(now().strftime('%y%-m%-d%-S'))
        super(Women, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Woman'
        verbose_name_plural = 'Women'
        ordering = ['time_update', 'title']


class Category(models.Model):
    name = models.CharField('Категория', max_length=128, db_index=True)
    slug = models.SlugField('URL', max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('women:category', kwargs={'cat_slug': self.slug})

    def not_empty(self):
        return Women.objects.filter(category_id=self.pk).exists()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['id', ]
