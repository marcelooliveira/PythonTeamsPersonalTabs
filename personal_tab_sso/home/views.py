# Create your views here.
from django.shortcuts import render
from .models import Book


def index(request):
    books_list = []
    books_list.append(Book('', 'Harry Potter and the Philosopher''s Stone', 'J. K. Rowling'))
    books_list.append(Book('', 'Lord of the Rings', 'J.R.Tolkien'))
    books_list.append(Book('', 'Game of Thrones', 'G.R.R.Martin'))
    context = {'books_list': books_list}
    return render(request, 'home/index.html', context=context)
