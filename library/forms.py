"""
Forms for Library Management System
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book, Author, Category, BorrowRecord, UserProfile


class UserRegisterForm(UserCreationForm):
    """User registration form with additional fields"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class BookForm(forms.ModelForm):
    """Form for creating and updating books"""
    class Meta:
        model = Book
        fields = ['title', 'author', 'categories', 'isbn', 'description', 
                  'publication_date', 'pages', 'available_copies', 'total_copies', 'cover_image']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class AuthorForm(forms.ModelForm):
    """Form for creating and updating authors"""
    class Meta:
        model = Author
        fields = ['name', 'bio', 'birth_date', 'nationality']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }


class CategoryForm(forms.ModelForm):
    """Form for creating and updating categories"""
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class BorrowRecordForm(forms.ModelForm):
    """Form for creating borrow records"""
    class Meta:
        model = BorrowRecord
        fields = ['book', 'due_date', 'notes']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile"""
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'date_of_birth', 'profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
