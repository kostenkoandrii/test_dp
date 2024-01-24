from django.core.paginator import EmptyPage, PageNotAnInteger
from django.db.models import Case, When, F, ExpressionWrapper, fields, Value, Q
from django.utils import timezone


class PaginatedQuerysetMixin:
    paginator_class = None
    paginate_by = None

    def get_queryset(self):
        pass

    def get_paginated_queryset(self, page):
        paginator = self.paginator_class(self.get_queryset(), self.paginate_by)

        try:
            paginated_page = paginator.page(page)
        except PageNotAnInteger:
            paginated_page = paginator.page(1)
        except EmptyPage:
            paginated_page = paginator.page(paginator.num_pages)

        return paginated_page


class LoanJournalAnnotationMixin:

    def get_loan_journal_annotation(self):
        annotation_data = {
            "status": Case(
                When(actual_return_date__isnull=False, then=Value('RETURNED')),
                When(actual_return_date__isnull=True, then=Value('IN USE')),
                output_field=fields.CharField()
            ),
            "expiration_status": Case(
                When(
                    Q(actual_return_date__isnull=True) & Q(planned_return_date__lt=timezone.now()),
                    then=Value("EXPIRED")
                ),
                When(
                    Q(actual_return_date__isnull=False) & Q(planned_return_date__gt=F('actual_return_date')),
                    then=Value("NOT EXPIRED")
                ),
                When(
                    Q(actual_return_date__isnull=False) & Q(planned_return_date__lt=F('actual_return_date')),
                    then=Value("EXPIRED")
                ),
                When(planned_return_date__gt=timezone.now(), then=Value("NOT EXPIRED")),
                output_field=fields.CharField()
            ),
            "days_left": ExpressionWrapper(
                F('planned_return_date') - timezone.now(),
                output_field=fields.DurationField()
            )
        }
        return annotation_data
