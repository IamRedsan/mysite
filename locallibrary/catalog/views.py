import datetime
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, BookInstance, Author, Genre
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, authenticate
from .forms import RenewBookForm, SignUpForm
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .constants import LoanStatus, ITEMS_PER_PAGE_BOOKLIST, ITEMS_PER_PAGE_COPIES, ITEMS_PER_PAGE_LOANBOOKS, AUTHORS_PER_PAGE, DEFAULT_DATE_OF_DEATH

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
    

class LoanedBooksByStaffListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    paginate_by = ITEMS_PER_PAGE_LOANBOOKS
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    context_object_name = "bookinstance_list"

    def get_queryset(self) -> QuerySet[Any]:
        return (
            super()
            .get_queryset()
            .filter(status__exact= LoanStatus.ON_LOAN.value)
            .order_by("due_back")
        )


@login_required
@permission_required("catalog.can_mark_returned", raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == "POST":
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data["renewal_date"]
            book_instance.save()
            return HttpResponseRedirect(reverse("my-borrowed"))
        else:
            proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
            form = RenewBookForm(initial={"renewal_date": proposed_renewal_date})

        context = {
            "form": form,
            "book_instance": book_instance,
        }
        return render(
            request=request,
            template_name="catalog/book_renew_librarian.html",
            context=context,
        )


class AuthorCreate(CreateView):
    model = Author
    fields = ["first_name", "last_name", "date_of_birth", "date_of_death"]
    initial = {"date_of_death": DEFAULT_DATE_OF_DEATH}


class AuthorUpdate(UpdateView):
    model = Author
    fields = ["first_name", "last_name", "date_of_birth", "date_of_death"]


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy("authors")


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = AUTHORS_PER_PAGE
    context_object_name = "author_list"
    template_name = "catalog/author_list.html"
    
class AuthorDetailView(generic.DetailView):
    model = Author
    def author_detail_view(request, primary_pkey):
        author = get_object_or_404(Author, pk= primary_pkey)
        context = {"author": author}
        return render(request=request, template_name="catalog/author_detail.html", context=context)

class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'catalog/sign_up.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        return render(request, 'catalog/sign_up.html', {'form': form})