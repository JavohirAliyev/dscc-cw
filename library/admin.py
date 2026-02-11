"""
Admin configuration for Library Management System
"""
from django.contrib import admin
from django.db import models
from .models import Author, Category, Book, BorrowRecord, UserProfile


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'nationality', 'birth_date', 'book_count', 'created_at']
    search_fields = ['name', 'nationality']
    list_filter = ['nationality', 'created_at']
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _book_count=models.Count('books', distinct=True)
        )
        return queryset
    
    @admin.display(ordering='_book_count', description='Books')
    def book_count(self, obj):
        return obj._book_count


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'book_count', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _book_count=models.Count('books', distinct=True)
        )
        return queryset
    
    @admin.display(ordering='_book_count', description='Books')
    def book_count(self, obj):
        return obj._book_count


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'available_copies', 'total_copies', 'publication_date', 'is_available']
    search_fields = ['title', 'isbn', 'author__name']
    list_filter = ['categories', 'author', 'publication_date', 'created_at']
    filter_horizontal = ['categories']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    list_select_related = ['author']
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('author').prefetch_related('categories')
        return queryset


@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'borrow_date', 'due_date', 'return_date', 'status', 'is_overdue']
    search_fields = ['user__username', 'book__title']
    list_filter = ['status', 'borrow_date', 'due_date']
    date_hierarchy = 'borrow_date'
    readonly_fields = ['borrow_date']
    list_select_related = ['user', 'book', 'book__author']
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('user', 'book', 'book__author')
        return queryset


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'created_at']
    search_fields = ['user__username', 'phone_number']
    list_filter = ['created_at']
    list_select_related = ['user']
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('user')
        return queryset