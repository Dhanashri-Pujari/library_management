from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.conf import settings
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from django.utils.module_loading import import_string
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from .forms import BookForm  
from django.db.utils import IntegrityError


def my_view(request):
    my_function = import_string("myapp.utils.some_function")  # Dynamically import
    result = my_function()  # Call the function
    return HttpResponse(f"Function Output: {result}")

User = get_user_model()  # Use the correct User model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User  # Use custom User model
        fields = ['email', 'password1', 'password2']

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after signup
    else:
        form = CustomUserCreationForm()
    return render(request, 'books/signup.html', {'form': form})

# User Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('book_list')  # Redirect after login
    else:
        form = AuthenticationForm()
    return render(request, 'books/login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Book List View (Protected)
@login_required(login_url='login')  # Redirect to login page if not logged in
def book_list_view(request):
    books = Book.objects.all()
    return render(request, "books/books.html", {"books": books})

# REST API for Books
class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

def create_book_view(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('book_list')  # Redirect after successful creation
            except IntegrityError:
                form.add_error('isbn', 'This ISBN already exists. Please use a unique ISBN.')
    else:
        form = BookForm()

    return render(request, 'books/create_book.html', {'form': form})

def update_book_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Redirect to the book list
    else:
        form = BookForm(instance=book)

    return render(request, 'books/update_book.html', {'form': form, 'book': book})

def delete_book_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect('book_list')  # Redirect to book list after deletion
    return render(request, 'books/book_delete.html', {'book': book})


def search_books(request):
    title_query = request.GET.get('title', '')
    books = Book.objects.filter(title__icontains=title_query).values('id', 'title', 'author', 'published_date')
    return JsonResponse(list(books), safe=False)