from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'book_id', 'author_name', 'price', 'is_published')
    search_fields = ('name', 'author_name')
    exclude = ('book_id',)
