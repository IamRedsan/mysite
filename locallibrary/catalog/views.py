from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from .models import Book, BookInstance, Author, Genre
from .constants import LoanStatus, ITEMS_PER_PAGE_BOOKLIST, ITEMS_PER_PAGE_COPIES
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(
        status__exact=LoanStatus.AVAILABLE.value
    ).count()  # __exact : field look up

    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits',1)
    request.session['num_visits'] = num_visits + 1
    
    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        "num_visits" : num_visits
    }

    return render(request, "index.html", context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = ITEMS_PER_PAGE_BOOKLIST
    context_object_name = "my_book_list"
    template_name = "catalog/book_list.html"

    def get_queryset(self):
        return super().get_queryset().order_by("title")
    
    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context (nếu muốn chèn thêm data vào)
        context["some_data"] = "This is just some data"
        return context


class BookDetailView(generic.DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["LoanStatus"] = LoanStatus.__members__
        return context

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    paginate_by = ITEMS_PER_PAGE_COPIES
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    context_object_name = "bookinstance_list"
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("book")
            .filter(borrower=self.request.user)
            .filter(status__exact= LoanStatus.ON_LOAN.value)
            .order_by("due_back"))
    
