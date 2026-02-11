"""
Views for Library Management System
Includes authentication, CRUD operations, and user management
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.cache import cache_page
from datetime import timedelta
from .models import Book, Author, Category, BorrowRecord, UserProfile
from .forms import UserRegisterForm, BookForm, AuthorForm, CategoryForm, BorrowRecordForm, UserProfileForm


@cache_page(60 * 5)  # Cache for 5 minutes
def home(request):
    """Home page view - displays recent books and statistics"""
    recent_books = Book.objects.select_related('author').prefetch_related('categories')[:6]
    total_books = Book.objects.count()
    total_authors = Author.objects.count()
    total_categories = Category.objects.count()
    
    context = {
        'recent_books': recent_books,
        'total_books': total_books,
        'total_authors': total_authors,
        'total_categories': total_categories,
    }
    return render(request, 'library/home.html', context)


def book_list(request):
    """Book list view with search and filter functionality"""
    from django.db.models import Count
    
    books = Book.objects.select_related('author').prefetch_related('categories')
    query = request.GET.get('q')
    category = request.GET.get('category')
    
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__name__icontains=query) |
            Q(isbn__icontains=query)
        )
    
    if category:
        books = books.filter(categories__id=category)
    
    # Pagination
    paginator = Paginator(books, 20)  # Show 20 books per page
    page = request.GET.get('page')
    
    try:
        books_page = paginator.page(page)
    except PageNotAnInteger:
        books_page = paginator.page(1)
    except EmptyPage:
        books_page = paginator.page(paginator.num_pages)
    
    # Optimize category query with book count
    categories = Category.objects.annotate(book_count=Count('books'))
    
    context = {
        'books': books_page,
        'categories': categories,
        'query': query,
        'selected_category': category,
    }
    return render(request, 'library/book_list.html', context)


def book_detail(request, pk):
    """Book detail view"""
    book = get_object_or_404(
        Book.objects.select_related('author').prefetch_related('categories'),
        pk=pk
    )
    user_has_borrowed = False
    
    if request.user.is_authenticated:
        user_has_borrowed = BorrowRecord.objects.filter(
            user=request.user,
            book=book,
            status='borrowed'
        ).exists()
    
    context = {
        'book': book,
        'user_has_borrowed': user_has_borrowed,
    }
    return render(request, 'library/book_detail.html', context)


@login_required
def book_create(request):
    """Create new book - CRUD Create operation"""
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" has been created successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()
    
    return render(request, 'library/book_form.html', {'form': form, 'action': 'Create'})


@login_required
def book_update(request, pk):
    """Update book - CRUD Update operation"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" has been updated successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    
    return render(request, 'library/book_form.html', {'form': form, 'action': 'Update', 'book': book})


@login_required
def book_delete(request, pk):
    """Delete book - CRUD Delete operation"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'Book "{title}" has been deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'library/book_confirm_delete.html', {'book': book})


@login_required
def borrow_book(request, pk):
    """Borrow a book with transaction safety"""
    from django.db import transaction
    
    # Use transaction and select_for_update to prevent race conditions
    with transaction.atomic():
        # Lock the book row for update
        book = get_object_or_404(
            Book.objects.select_for_update(),
            pk=pk
        )
        
        # Check if user already borrowed this book
        existing_borrow = BorrowRecord.objects.filter(
            user=request.user,
            book=book,
            status='borrowed'
        ).exists()
        
        if existing_borrow:
            messages.warning(request, 'You have already borrowed this book!')
            return redirect('book_detail', pk=pk)
        
        if not book.is_available():
            messages.error(request, 'This book is not available for borrowing!')
            return redirect('book_detail', pk=pk)
        
        # Create borrow record
        due_date = timezone.now() + timedelta(days=14)  # 2 weeks loan
        BorrowRecord.objects.create(
            user=request.user,
            book=book,
            due_date=due_date,
            status='borrowed'
        )
        
        # Update available copies
        book.available_copies -= 1
        book.save()
    
    messages.success(request, f'You have successfully borrowed "{book.title}"!')
    return redirect('my_borrowed_books')


@login_required
def my_borrowed_books(request):
    """View user's borrowed books"""
    borrow_records = BorrowRecord.objects.filter(
        user=request.user
    ).select_related('book', 'book__author').prefetch_related('book__categories')
    
    # Pagination
    paginator = Paginator(borrow_records, 10)  # Show 10 records per page
    page = request.GET.get('page')
    
    try:
        records_page = paginator.page(page)
    except PageNotAnInteger:
        records_page = paginator.page(1)
    except EmptyPage:
        records_page = paginator.page(paginator.num_pages)
    
    context = {
        'borrow_records': records_page,
    }
    return render(request, 'library/my_borrowed_books.html', context)


@login_required
def return_book(request, pk):
    """Return a borrowed book with transaction safety"""
    from django.db import transaction
    
    with transaction.atomic():
        # Lock both records for update
        borrow_record = get_object_or_404(
            BorrowRecord.objects.select_related('book').select_for_update(),
            pk=pk,
            user=request.user
        )
        
        if borrow_record.status != 'borrowed':
            messages.warning(request, 'This book has already been returned!')
            return redirect('my_borrowed_books')
        
        # Update borrow record
        borrow_record.return_date = timezone.now()
        borrow_record.status = 'returned'
        borrow_record.save()
        
        # Update available copies with select_for_update
        book = Book.objects.select_for_update().get(pk=borrow_record.book.pk)
        book.available_copies += 1
        book.save()
    
    messages.success(request, f'You have successfully returned "{book.title}"!')
    return redirect('my_borrowed_books')


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'library/register.html', {'form': form})


def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'library/login.html')


@login_required
def user_logout(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully!')
    return redirect('home')


@login_required
def user_profile(request):
    """User profile view"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=profile)
    
    borrow_count = BorrowRecord.objects.filter(user=request.user).count()
    active_borrows = BorrowRecord.objects.filter(user=request.user, status='borrowed').count()
    
    context = {
        'form': form,
        'profile': profile,
        'borrow_count': borrow_count,
        'active_borrows': active_borrows,
    }
    return render(request, 'library/user_profile.html', context)


def author_list(request):
    """Author list view"""
    authors = Author.objects.prefetch_related('books').all()
    query = request.GET.get('q')
    
    if query:
        authors = authors.filter(Q(name__icontains=query))
    
    # Pagination
    paginator = Paginator(authors, 20)  # Show 20 authors per page
    page = request.GET.get('page')
    
    try:
        authors_page = paginator.page(page)
    except PageNotAnInteger:
        authors_page = paginator.page(1)
    except EmptyPage:
        authors_page = paginator.page(paginator.num_pages)
    
    context = {
        'authors': authors_page,
        'query': query,
    }
    return render(request, 'library/author_list.html', context)


def author_detail(request, pk):
    """Author detail view"""
    author = get_object_or_404(Author.objects.prefetch_related('books'), pk=pk)
    books = author.books.select_related('author').prefetch_related('categories')
    
    context = {
        'author': author,
        'books': books,
    }
    return render(request, 'library/author_detail.html', context)
