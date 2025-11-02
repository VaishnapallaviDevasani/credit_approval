from django.urls import path
from .views import CustomerListCreateView, LoanListCreateView

urlpatterns = [
    path('customers/', CustomerListCreateView.as_view(), name='customer-list'),
    path('loans/', LoanListCreateView.as_view(), name='loan-list'),
]
from .views import RegisterCustomerView
urlpatterns += [
    path('register/', RegisterCustomerView.as_view(), name='register-customer'),
]
from .views import LoanEligibilityView

urlpatterns += [
    path('check-eligibility/', LoanEligibilityView.as_view(), name='check-eligibility'),
]


from .views import CreateLoanView
urlpatterns += [
    path('create-loan/', CreateLoanView.as_view(), name='create-loan'),
]



from .views import ViewLoanDetail

urlpatterns += [
    path('view-loan/<int:loanid>/', ViewLoanDetail.as_view(), name='view-loan'),
]


from .views import ViewLoansByCustomer

urlpatterns += [
    path('view-loans/<int:customerid>/', ViewLoansByCustomer.as_view(), name='view-loans'),
]
