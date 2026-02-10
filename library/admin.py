"""
Admin configuration for Library Management System
"""
from django.contrib import admin
from .models import Author, Category, Book, BorrowRecord, UserProfile


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'nationality', 'birth_date', 'get_book_count', 'created_at']
    search_fields = ['name', 'nationality']
    list_filter = ['nationality', 'created_at']
    date_hierarchy = 'created_at'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_book_count', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'available_copies', 'total_copies', 'publication_date', 'is_available']
    search_fields = ['title', 'isbn', 'author__name']
    list_filter = ['categories', 'author', 'publication_date', 'created_at']
    filter_horizontal = ['categories']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']


@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'borrow_date', 'due_date', 'return_date', 'status', 'is_overdue']
    search_fields = ['user__username', 'book__title']
    list_filter = ['status', 'borrow_date', 'due_date']
    date_hierarchy = 'borrow_date'
    readonly_fields = ['borrow_date']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'created_at']
    search_fields = ['user__username', 'phone_number']
    list_filter = ['created_at']
