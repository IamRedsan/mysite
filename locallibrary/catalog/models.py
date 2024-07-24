from typing import Iterable
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .constants import LoanStatus
from django.core.exceptions import ValidationError
import uuid


# Create your models here.
class Genre(models.Model):
    name = models.CharField(
        max_length=200, help_text=_("Enter the book genre (e.g: SF, Romantic,...) ")
    )

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200, help_text=_("Enter the title of the book"))
    author = models.ForeignKey(
        "Author",
        on_delete=models.SET_NULL,
        null=True,
        help_text=_("Select the author of the book"),
    )
    summary = models.TextField(
        max_length=1000, help_text=_("Enter a brief description of the book")
    )
    isbn = models.CharField(
        "ISBN",
        max_length=13,
        unique=True,
        help_text=_(
            'Enter the 13-character ISBN number of the book. See <a href="https://www.isbn-international.org/content/what-isbn">ISBN information</a> for more details.'
        ),
    )
    genre = models.ManyToManyField(
        Genre, help_text=_("Select one or more genres for this book")
    )

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])

    def display_genre(self):
        return ", ".join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = _("Genre")


class BookInstance(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text=_("Unique ID for this particular book across the whole library"),
    )
    book = models.ForeignKey(
        "Book",
        on_delete=models.RESTRICT,
        help_text=_("Select the book for this instance"),
    )
    imprint = models.CharField(
        max_length=200,
        help_text=_(
            "Enter the imprint information (e.g., publisher, publication date)"
        ),
    )
    due_back = models.DateField(
        null=True,
        blank=True,
        help_text=_("Enter the date when the book is due to be returned"),
    )
    status = models.CharField(
        max_length=1,
        choices=LoanStatus.choices(),
        blank=True,
        default="m",
        help_text=_("Select the current status of the book"),
    )

    class Meta:
        ordering = ["due_back"]

    def __str__(self) -> str:
        return f"{self.id} : {self.book.title}"


class Author(models.Model):
    first_name = models.CharField(
        max_length=100, help_text=_("Enter the author's first name")
    )
    last_name = models.CharField(
        max_length=100, help_text=_("Enter the author's last name")
    )
    date_of_birth = models.DateField(
        null=True, blank=True, help_text=_("Enter the author's date of birth")
    )
    date_of_death = models.DateField(
        _("Died"),
        null=True,
        blank=True,
        help_text=_("Enter the author's date of death, if applicable"),
    )

    class Meta:
        ordering = ["last_name", "first_name"]

    def clean(self):
        if self.date_of_birth and self.date_of_death:
            if self.date_of_death <= self.date_of_birth:
                raise ValidationError(_("Date of death must be after date of birth."))
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    
    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.id)])

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name}"
