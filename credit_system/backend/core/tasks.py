# backend/core/tasks.py

from celery import shared_task
import pandas as pd
from .models import Customer, Loan
from datetime import datetime

@shared_task
def load_excel_data():
    customer_df = pd.read_excel("customer_data.xlsx")
    loan_df = pd.read_excel("loan_data.xlsx")

    for _, row in customer_df.iterrows():
        Customer.objects.update_or_create(
            customer_id=row['customer_id'],
            defaults={
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'phone_number': str(row['phone_number']),
                'monthly_income': row['monthly_salary'],
                'approved_limit': row['approved_limit'],
                'current_debt': row['current_debt'],
                'age': 0,  # Age not in sheet, defaulting to 0
            }
        )

    for _, row in loan_df.iterrows():
        Loan.objects.update_or_create(
            loan_id=row['loan_id'],
            defaults={
                'customer_id': row['customer id'],
                'loan_amount': row['loan amount'],
                'tenure': row['tenure'],
                'interest_rate': row['interest rate'],
                'monthly_installment': row['monthly repayment (emi)'],
                'emis_paid_on_time': row['EMIs paid on time'],
                'start_date': pd.to_datetime(row['start date']).date(),
                'end_date': pd.to_datetime(row['end date']).date(),
            }
        )
