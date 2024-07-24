from django.contrib import admin
from .models import Author, Genre, Book, BookInstance


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "date_of_birth", "date_of_death")
    fields = ["first_name", "last_name", ("date_of_birth", "date_of_death")]


admin.site.register(Author, AuthorAdmin)


class BookInstanceInline(admin.TabularInline):
    model = BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "display_genre")
    inlines = [BookInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ("status", "due_back")
    fieldsets = (
        ("Information", {"fields": ("book", "imprint", "id")}),
        ("Availability", {"fields": ("status", "due_back")}),
    )


# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)
