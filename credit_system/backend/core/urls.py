from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_customer),
    path('customers/', views.get_customers),
    path('loan-request/', views.request_loan),
    path('loan-status/<int:loan_id>/', views.loan_status),  
]
