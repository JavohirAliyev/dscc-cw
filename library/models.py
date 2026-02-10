"""
Models for Library Management System
Includes: Author, Category, Book, BorrowRecord
Relationships: Many-to-One (Book-Author), Many-to-Many (Book-Category, User-Book via BorrowRecord)
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Author(models.Model):
    """Author model - has one-to-many relationship with Book"""
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_book_count(self):
        return self.books.count()


class Category(models.Model):
    """Category model - has many-to-many relationship with Book"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_book_count(self):
        return self.books.count()


class Book(models.Model):
    """
    Book model with relationships:
    - Many-to-One with Author (Foreign Key)
    - Many-to-Many with Category
    """
    title = models.CharField(max_length=300)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )  # Many-to-One relationship
    categories = models.ManyToManyField(
        Category,
        related_name='books',
        blank=True
    )  # Many-to-Many relationship
    isbn = models.CharField(max_length=13, unique=True)
    description = models.TextField(blank=True)
    publication_date = models.DateField()
    pages = models.IntegerField(default=0)
    available_copies = models.IntegerField(default=1)
    total_copies = models.IntegerField(default=1)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.author.name}"

    def is_available(self):
        return self.available_copies > 0


class BorrowRecord(models.Model):
    """
    BorrowRecord model - creates Many-to-Many relationship between User and Book
    Tracks book borrowing history
    """
    STATUS_CHOICES = [
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='borrow_records'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='borrow_records'
    )
    borrow_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='borrowed'
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-borrow_date']

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.status})"

    def is_overdue(self):
        if self.status == 'borrowed' and self.due_date < timezone.now():
            return True
        return False


class UserProfile(models.Model):
    """Extended user profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
