from django.contrib import admin
from blog import models


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('get_image', 'title', 'author', 'get_category', 'status', 'jalali_date')
    list_filter = ('category', 'status', 'created')
    list_editable = ('status',)
    search_fields = ('title', 'description')
    ordering = ('-created',)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'status')
    list_editable = ('status',)
    search_fields = ('title',)
    list_filter = ('created', 'status')
