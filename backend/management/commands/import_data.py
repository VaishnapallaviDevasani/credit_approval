from django.core.management.base import BaseCommand
import pandas as pd
from backend.models import Customer, Loan

class Command(BaseCommand):
    help = 'Import customer and loan data from Excel files'

    def handle(self, *args, **kwargs):
        # Read customers Excel
        cust_df = pd.read_excel('customer_data.xlsx')
        for _, row in cust_df.iterrows():
            Customer.objects.get_or_create(
                customer_id=row['Customer ID'],
                defaults={
                    'first_name': row['First Name'],
                    'last_name': row['Last Name'],
                    'age': row['Age'],
                    'phone_number': str(row['Phone Number']),
                    'monthly_salary': row['Monthly Salary'],
                    'approved_limit': row['Approved Limit'],
                }
            )
        self.stdout.write(self.style.SUCCESS('Imported customers!'))

        # Read loans Excel
        loan_df = pd.read_excel('loan_data.xlsx')
        for _, row in loan_df.iterrows():
            customer = Customer.objects.get(customer_id=row['Customer ID'])
            Loan.objects.get_or_create(
                loan_id=row['Loan ID'],
                customer=customer,
                defaults={
                    'loan_amount': row['Loan Amount'],
                    'tenure': row['Tenure'],
                    'interest_rate': row['Interest Rate'],
                    'monthly_payment': row['Monthly payment'],
                    'emis_paid_on_time': row['EMIs paid on Time'],
                    'date_of_approval': row['Date of Approval'],
                    'end_date': row['End Date'],
                }
            )
        self.stdout.write(self.style.SUCCESS('Imported loans!'))
