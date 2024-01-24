from datetime import timedelta

from library.mixins import PaginatedQuerysetMixin, LoanJournalAnnotationMixin
from library.models import Book, Client, BookLoanJournal

from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.db.models import Q


class BookListView(PaginatedQuerysetMixin, ListView):
    model = Book
    template_name = 'books.html'
    context_object_name = 'books'
    paginate_by = 5
    paginator_class = Paginator

    def get_queryset(self):
        q = Q()

        book = self.request.GET.get('book')
        article_name = self.request.GET.get('article_name')
        author = self.request.GET.get('author')

        q.add(Q(name__icontains=book), q.AND) if book else ...
        q.add(Q(summary__article_name__icontains=article_name), q.AND) if article_name else ...
        q.add(
            Q(Q(author__first_name__icontains=author) | Q(author__first_name__icontains=author)), q.AND
        ) if author else ...

        queryset = self.model.objects.filter(q).select_related('author').prefetch_related('summary')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page = self.request.GET.get('page')
        context['books'] = self.get_paginated_queryset(page)

        return context


class LoanJournalView(LoanJournalAnnotationMixin, PaginatedQuerysetMixin, ListView):
    model = BookLoanJournal
    template_name = 'loan_journal.html'
    context_object_name = 'loan_journal'
    paginate_by = 5
    paginator_class = Paginator

    def get_queryset(self):
        q = Q()

        book = self.request.GET.get('book')
        client = self.request.GET.get('client_name')
        status = self.request.GET.get('status')
        exp_status = self.request.GET.get('exp_status')
        days_left = self.request.GET.get('days_left')

        q.add(Q(book__name__icontains=book), q.AND) if book else ...
        q.add(Q(status=status), q.AND) if status else ...
        q.add(Q(expiration_status=exp_status), q.AND) if exp_status else ...
        q.add(Q(days_left__lt=timedelta(days=int(days_left))), q.AND) if days_left and days_left.isdigit() else ...
        q.add(
            Q(Q(client__first_name__icontains=client) | Q(client__last_name__icontains=client)), q.AND
        ) if client else ...

        annotation = self.get_loan_journal_annotation()
        queryset = self.model.objects.all().order_by('client__first_name').annotate(**annotation).filter(q)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page = self.request.GET.get('page')
        context['loan_journal'] = self.get_paginated_queryset(page)

        return context


class ClientDetailView(DetailView):
    model = Client
    template_name = 'client_details.html'


class ClientsListView(PaginatedQuerysetMixin, ListView):
    model = Client
    template_name = 'clients.html'
    context_object_name = 'clients'
    paginate_by = 5
    paginator_class = Paginator

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page = self.request.GET.get('page')
        context[self.context_object_name] = self.get_paginated_queryset(page)

        return context


class ClientsLoanJournalView(LoanJournalAnnotationMixin, PaginatedQuerysetMixin, ListView):
    model = BookLoanJournal
    template_name = 'client_loan_journal.html'
    context_object_name = 'loan_journal'
    paginate_by = 5
    paginator_class = Paginator

    def get_queryset(self):
        client_id = self.kwargs.get('pk')
        annotation = self.get_loan_journal_annotation()

        return self.model.objects.filter(client__id=client_id).annotate(**annotation)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page = self.request.GET.get('page')
        context[self.context_object_name] = self.get_paginated_queryset(page)

        return context
