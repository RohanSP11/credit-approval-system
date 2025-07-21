import pandas as pd
import os
from django.core.management.base import BaseCommand
from core.models import Customer, Loan
from datetime import datetime

class Command(BaseCommand):
    help = 'Import customer and loan data from Excel files'

    def handle(self, *args, **kwargs):
      
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        customer_file = os.path.join(base_dir, '..', 'customer_data.xlsx')
        loan_file = os.path.join(base_dir, '..', 'loan_data.xlsx')

        
        customer_df = pd.read_excel(customer_file)
        customer_df.columns = customer_df.columns.str.strip()  

        loan_df = pd.read_excel(loan_file)
        loan_df.columns = loan_df.columns.str.strip()

        
        for _, row in customer_df.iterrows():
            print(f"Inserting Customer ID {row['Customer ID']} with age: {row['Age']}")
            Customer.objects.update_or_create(
                customer_id=row['Customer ID'],
                defaults={
                    'first_name': row['First Name'],
                    'last_name': row['Last Name'],
                    'age': row['Age'],
                    'phone_number': row['Phone Number'],
                    'monthly_salary': row['Monthly Salary'],
                    'approved_limit': row['Approved Limit'],
                }
            )

        
        for _, row in loan_df.iterrows():
            customer = Customer.objects.get(customer_id=row['Customer ID'])
            Loan.objects.update_or_create(
                loan_id=row['Loan ID'],
                defaults={
                    'customer': customer,
                    'loan_amount': row['Loan Amount'],
                    'tenure': row['Tenure'],
                    'interest_rate': row['Interest Rate'],
                    'monthly_payment': row['Monthly payment'],
                    'emis_paid_on_time': row['EMIs paid on Time'],
                    'start_date': pd.to_datetime(row['Date of Approval']).date(),
                    'end_date': pd.to_datetime(row['End Date']).date(),
                }
            )

        self.stdout.write(self.style.SUCCESS('✅ Excel data imported successfully.'))
