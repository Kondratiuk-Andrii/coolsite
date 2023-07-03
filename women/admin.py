from django.contrib import admin
from django.utils.safestring import mark_safe

from women.models import Category, Women


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_html_photo', 'time_create', 'is_published',)
    list_display_links = ('title',)
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create',)
    fields = ('title', 'slug', 'category', 'content', 'get_html_photo', 'is_published', 'time_create', 'time_update',)
    readonly_fields = ('get_html_photo', 'time_create', 'time_update',)
    prepopulated_fields = {'slug': ('title',)}

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f'<img src="{object.photo.url}" width=150')

    get_html_photo.short_description = 'Изображения'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.site_title = 'Админ панель сайта о женщинах'
admin.site.site_header = 'Админ панель сайта о женщинах'
