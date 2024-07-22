from typing import Any
from django.shortcuts import render, get_object_or_404
from .models import Book, BookInstance, Author, Genre
from django.views import generic


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


class BookListView(generic.ListView):
    model = Book
    paginate_by = 2
    context_object_name = "my_book_list"
    # queryset = Book.objects.filter(title__icontains="war")[:5]
    template_name = "catalog/book_list.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context (nếu muốn chèn thêm data vào)
        context["some_data"] = "This is just some data"
        return context


class BookDetailView(generic.DetailView):
    model = Book

    def book_detail_view(request, primary_key):
        book = get_object_or_404(Book, pk=primary_key)

        return render(request, "catalog/book_detail.html", context={"book": book})
