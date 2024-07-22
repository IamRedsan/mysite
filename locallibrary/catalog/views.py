from django.shortcuts import render
from .models import Book, BookInstance, Author, Genre


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available Books
    num_instances_available = BookInstance.objects.filter(
        status__exact="a"
    ).count()  # __exact : field look up

    # The all() is implied by default
    num_authors = Author.objects.count()

    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
    }

    return render(request, "index.html", context=context)