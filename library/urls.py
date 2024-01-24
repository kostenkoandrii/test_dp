from django.conf.urls import url
from library.views import BookListView, LoanJournalView, ClientDetailView, ClientsListView, ClientsLoanJournalView

urlpatterns = [
    url(r'clients/(?P<pk>\d+)/loan-journal', ClientsLoanJournalView.as_view(), name='client_loan_journal'),
    url(r'clients/(?P<pk>\d+)/$', ClientDetailView.as_view(), name='client_detail'),
    url(r'clients/', ClientsListView.as_view(), name='clients_list'),
    url('books/', BookListView.as_view(), name='book_list'),
    url('loan-journal/', LoanJournalView.as_view(), name='loan_journal'),
]
