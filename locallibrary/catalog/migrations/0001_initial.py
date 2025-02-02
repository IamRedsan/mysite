# Generated by Django 5.0.7 on 2024-07-24 07:45

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        help_text="Enter the author's first name", max_length=100
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        help_text="Enter the author's last name", max_length=100
                    ),
                ),
                (
                    "date_of_birth",
                    models.DateField(
                        blank=True,
                        help_text="Enter the author's date of birth",
                        null=True,
                    ),
                ),
                (
                    "date_of_death",
                    models.DateField(
                        blank=True,
                        help_text="Enter the author's date of death, if applicable",
                        null=True,
                        verbose_name="Died",
                    ),
                ),
            ],
            options={
                "ordering": ["last_name", "first_name"],
            },
        ),
        migrations.CreateModel(
            name="Genre",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Enter the book genre (e.g: SF, Romantic,...)",
                        max_length=200,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Enter the title of the book", max_length=200
                    ),
                ),
                (
                    "summary",
                    models.TextField(
                        help_text="Enter a brief description of the book",
                        max_length=1000,
                    ),
                ),
                (
                    "isbn",
                    models.CharField(
                        help_text='Enter the 13-character ISBN number of the book. See <a href="https://www.isbn-international.org/content/what-isbn">ISBN information</a> for more details.',
                        max_length=13,
                        unique=True,
                        verbose_name="ISBN",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        help_text="Select the author of the book",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="catalog.author",
                    ),
                ),
                (
                    "genre",
                    models.ManyToManyField(
                        help_text="Select one or more genres for this book",
                        to="catalog.genre",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BookInstance",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        help_text="Unique ID for this particular book across the whole library",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "imprint",
                    models.CharField(
                        help_text="Enter the imprint information (e.g., publisher, publication date)",
                        max_length=200,
                    ),
                ),
                (
                    "due_back",
                    models.DateField(
                        blank=True,
                        help_text="Enter the date when the book is due to be returned",
                        null=True,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("m", "Maintenance"),
                            ("o", "On loan"),
                            ("a", "Available"),
                            ("r", "Reserved"),
                        ],
                        default="m",
                        help_text="Select the current status of the book",
                        max_length=1,
                    ),
                ),
                (
                    "book",
                    models.ForeignKey(
                        help_text="Select the book for this instance",
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="catalog.book",
                    ),
                ),
            ],
            options={
                "ordering": ["due_back"],
            },
        ),
    ]
