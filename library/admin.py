from django.contrib import admin

from library.models import Author, Client, BookLoanJournal, Book, BookSummary

admin.site.register(Author)
admin.site.register(Client)
admin.site.register(BookLoanJournal)
admin.site.register(Book)
admin.site.register(BookSummary)
