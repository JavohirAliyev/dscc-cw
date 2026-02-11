# Generated migration for performance optimization
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        # Add composite index for common book queries
        migrations.AddIndex(
            model_name='book',
            index=models.Index(fields=['available_copies', '-created_at'], name='library_book_avail_idx'),
        ),
        # Add index for author name lookups (case-insensitive searches)
        migrations.AddIndex(
            model_name='author',
            index=models.Index(fields=['name', 'nationality'], name='library_author_name_nat_idx'),
        ),
        # Add composite index for user borrow status queries
        migrations.AddIndex(
            model_name='borrowrecord',
            index=models.Index(fields=['user', 'status', '-borrow_date'], name='library_borrow_usr_stat_idx'),
        ),
        # Add index for overdue book queries
        migrations.AddIndex(
            model_name='borrowrecord',
            index=models.Index(fields=['status', '-due_date'], name='library_borrow_overdue_idx'),
        ),
    ]
