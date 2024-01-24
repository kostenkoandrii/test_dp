from django.db import models


class Client(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=13)
    address = models.CharField(max_length=225)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class BookLoanJournal(models.Model):
    book = models.ForeignKey('library.Book', related_name='loan_records', on_delete=models.CASCADE)
    client = models.ForeignKey('library.Client', related_name='loan_records', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    planned_return_date = models.DateField(null=False, blank=False)
    actual_return_date = models.DateField(null=True, blank=True)


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(max_length=50)


class Book(models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey(
        'library.Author',
        related_name='books',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("name", "author")

    def __str__(self):
        return self.name


class BookSummary(models.Model):
    page_number = models.IntegerField(null=False, blank=False)
    article_name = models.CharField(max_length=255, null=False, blank=False)
    book = models.ForeignKey(
        'library.Book',
        related_name='summary',
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    class Meta:
        unique_together = ("article_name", "book")

    def __str__(self):
        return 'Summary for {}'.format(self.book.name)
