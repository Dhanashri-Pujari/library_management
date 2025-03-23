from django.contrib.auth.models import AbstractUser,Group, Permission
from django.db import models

# Custom User Model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = None  # Remove default username
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "books_user"  # Explicitly set table name

    def __str__(self):
        return self.email
    



class Book(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)  # Manually assign ID
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField()
    available = models.BooleanField(default=True)


    def save(self, *args, **kwargs):
        if not self.id:  # Assign ID only if not provided
            existing_ids = list(Book.objects.values_list('id', flat=True))
            if existing_ids:
                # Find the smallest missing ID
                missing_ids = [i for i in range(1, max(existing_ids) + 2) if i not in existing_ids]
                self.id = missing_ids[0]  # Assign the smallest available ID
            else:
                self.id = 1  # First book gets ID 1
        super().save(*args, **kwargs)