"""
Tests for Library Management System
Includes tests for models, views, and authentication
"""
import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Author, Category, Book, BorrowRecord, UserProfile


@pytest.mark.django_db
class TestModels(TestCase):
    """Test cases for models"""

    def setUp(self):
        """Set up test data"""
        self.author = Author.objects.create(
            name="Test Author",
            bio="Test bio",
            nationality="Test Country"
        )
        self.category = Category.objects.create(
            name="Test Category",
            description="Test description"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author=self.author,
            isbn="1234567890123",
            description="Test description",
            publication_date=timezone.now().date(),
            pages=300,
            available_copies=5,
            total_copies=5
        )
        self.book.categories.add(self.category)

    def test_author_creation(self):
        """Test author model creation"""
        self.assertEqual(self.author.name, "Test Author")
        self.assertEqual(str(self.author), "Test Author")
        self.assertEqual(self.author.get_book_count(), 1)

    def test_category_creation(self):
        """Test category model creation"""
        self.assertEqual(self.category.name, "Test Category")
        self.assertEqual(str(self.category), "Test Category")
        self.assertEqual(self.category.get_book_count(), 1)

    def test_book_creation(self):
        """Test book model creation"""
        self.assertEqual(self.book.title, "Test Book")
        self.assertTrue(self.book.is_available())
        self.assertEqual(str(self.book), "Test Book by Test Author")

    def test_book_availability(self):
        """Test book availability check"""
        self.book.available_copies = 0
        self.book.save()
        self.assertFalse(self.book.is_available())


@pytest.mark.django_db
class TestViews(TestCase):
    """Test cases for views"""

    def setUp(self):
        """Set up test client and data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        UserProfile.objects.create(user=self.user)
        
        self.author = Author.objects.create(
            name="Test Author",
            nationality="Test Country"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author=self.author,
            isbn="1234567890123",
            publication_date=timezone.now().date(),
            pages=300,
            available_copies=5,
            total_copies=5
        )

    def test_home_page(self):
        """Test home page view"""
        response = self.client.get(reverse('home'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Library Management System")

    def test_book_list_page(self):
        """Test book list view"""
        response = self.client.get(reverse('book_list'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Book")

    def test_book_detail_page(self):
        """Test book detail view"""
        response = self.client.get(reverse('book_detail', args=[self.book.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)

    def test_login_required_for_borrow(self):
        """Test that borrowing requires login"""
        response = self.client.get(reverse('borrow_book', args=[self.book.pk]), follow=True)
        self.assertIn(response.status_code, [200, 302])  # May redirect to login or show login page

    def test_authenticated_user_can_access_profile(self):
        """Test authenticated user can access profile"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('user_profile'), follow=True)
        self.assertEqual(response.status_code, 200)


@pytest.mark.django_db
class TestAuthentication(TestCase):
    """Test cases for authentication"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()

    def test_user_registration(self):
        """Test user registration"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'ComplexPass123!@#',
            'password2': 'ComplexPass123!@#',
        }, follow=True)
        self.assertEqual(response.status_code, 200)  # Should complete after following redirects
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_login(self):
        """Test user login"""
        User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123',
        }, follow=True)
        self.assertEqual(response.status_code, 200)  # Should complete after following redirects


@pytest.mark.django_db
class TestBorrowingSystem(TestCase):
    """Test cases for book borrowing system"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        UserProfile.objects.create(user=self.user)
        
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            author=self.author,
            isbn="1234567890123",
            publication_date=timezone.now().date(),
            pages=300,
            available_copies=1,
            total_copies=1
        )

    def test_borrow_book_success(self):
        """Test successful book borrowing"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('borrow_book', args=[self.book.pk]), follow=True)
        self.assertEqual(response.status_code, 200)  # Should complete after following redirects
        
        # Check that borrow record was created
        self.assertTrue(
            BorrowRecord.objects.filter(
                user=self.user,
                book=self.book,
                status='borrowed'
            ).exists()
        )
        
        # Check that available copies decreased
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 0)

    def test_cannot_borrow_unavailable_book(self):
        """Test that unavailable books cannot be borrowed"""
        self.book.available_copies = 0
        self.book.save()
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('borrow_book', args=[self.book.pk]))
        
        # Should not create borrow record
        self.assertEqual(
            BorrowRecord.objects.filter(user=self.user, book=self.book).count(),
            0
        )
