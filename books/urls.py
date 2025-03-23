from django.urls import path
from books.views import signup_view, login_view, logout_view, book_list_view, BookListCreateAPIView, BookRetrieveUpdateDestroyAPIView,create_book_view,update_book_view,delete_book_view,search_books


urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('books/', book_list_view, name='book_list'),
    path('books/create_book/', create_book_view, name='create_book'),
    path('books/update_book/', update_book_view, name='update_book'),
    path('books/delete_book/', delete_book_view, name='delete_book'),
    path('api/books/', search_books, name='search_books'),

    # API Endpoints
    path('api/books/', BookListCreateAPIView.as_view(), name='api_books'),
    path('api/books/<int:pk>/', BookRetrieveUpdateDestroyAPIView.as_view(), name='api_book_detail'),
    path('books/update/<int:pk>/', update_book_view, name='update_book'),  # Update book
    path('books/delete/<int:pk>/', delete_book_view, name='delete_book'),  # Delete book


]
