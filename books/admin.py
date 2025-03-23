from django.contrib import admin
from .models import User, Book

admin.site.register(User)  # Register User model

@admin.register(Book)  # ✅ Correct way to register Book
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'available')
    search_fields = ('title', 'author')
