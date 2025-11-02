from django.shortcuts import render
from rest_framework import generics
from .models import Customer, Loan
from .serializers import CustomerSerializer, LoanSerializer

class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class LoanListCreateView(generics.ListCreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer

class RegisterCustomerView(APIView):
    def post(self, request):
        data = request.data
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        age = data.get('age')
        monthlyincome = data.get('monthlyincome')
        phonenumber = data.get('phonenumber')
        #the rule
        approvedlimit = round(36 * monthlyincome, -5)
        customer = Customer.objects.create(
            first_name=firstname, last_name=lastname, age=age,
            monthly_salary=monthlyincome, approved_limit=approvedlimit,
            phone_number=phonenumber
        )

        return Response({
            "customerid": customer.customer_id,
            "name": f"{firstname} {lastname}",
            "age": age,
            "monthlyincome": monthlyincome,
            "approvedlimit": approvedlimit,
            "phonenumber": phonenumber
        }, status=status.HTTP_201_CREATED)
from .models import Customer, Loan
from django.db.models import Sum
import datetime

class LoanEligibilityView(APIView):
    def post(self, request):
        data = request.data
        customer_id = data.get('customerid')
        requested_amount = data.get('loanamount')
        requested_interest = data.get('interest_rate')
        tenure = data.get('tenure')

        # Fetch customer and their loan history
        try:
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        past_loans = Loan.objects.filter(customer=customer)

        # Calculate credit rating logic
        paid_on_time = sum([loan.emis_paid_on_time for loan in past_loans])
        num_loans = past_loans.count()
        current_year = datetime.date.today().year
        loans_this_year = past_loans.filter(date_of_approval__year=current_year).count()
        total_approved = past_loans.aggregate(Sum('loan_amount'))['loan_amount__sum'] or 0

        # Example rating formula (customize as per assignment rules):
        creditrating = 0
        if customer.current_debt > customer.approved_limit:
            creditrating = 0
        else:
            # Add more business logic here for actual rating
            creditrating += min(paid_on_time / max(num_loans,1) * 70, 70)
            creditrating += min(loans_this_year * 10, 10)
            creditrating += min(float(total_approved) / (float(customer.approved_limit) or 1) * 20, 20)
        # Interest slab business logic
        corrected_interest = requested_interest
        if creditrating >= 50:
            approved = True
            corrected_interest = requested_interest
        elif 50 > creditrating >= 30:
            approved = True
            corrected_interest = 12.0
        elif 30 > creditrating >= 10:
            approved = True
            corrected_interest = 16.0
        else:
            approved = False
            corrected_interest = None

        # If EMIs > 50% salary, reject
        current_emis_total = sum([loan.monthly_payment for loan in past_loans])
        if current_emis_total > (float(customer.monthly_salary) * 0.5):
            approved = False

        # If not approved, return rejection
        if not approved:
            return Response({
                "customerid": customer_id,
                "approval": False,
                "reason": "Loan not approved due to credit rating/EMIs.",
            }, status=status.HTTP_200_OK)

        # Calculate monthly installment (basic, adjust with compound formula if needed)
        monthlyinstallment = (requested_amount * (1 + corrected_interest/100)**(tenure/12)) / tenure

        return Response({
            "customerid": customer_id,
            "approval": True,
            "interestrate": requested_interest,
            "correctedinterestrate": corrected_interest,
            "tenure": tenure,
            "monthlyinstallment": int(monthlyinstallment)
        }, status=status.HTTP_200_OK)
    

    from .models import Loan
import datetime  # Make sure this is imported!
from decimal import Decimal

class CreateLoanView(APIView):
    def post(self, request):
        data = request.data
        customer_id = data.get('customerid')
        loan_amount = float(data.get('loanamount'))        # Convert to float here
        interest_rate = float(data.get('interest_rate'))   # Convert to float here
        tenure = int(data.get('tenure'))                   # Ensure this is int

        # Fetch customer
        try:
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # Apply eligibility logic (reuse code from eligibility API)
        # For teaching, here’s a simplified version:
        approval = True
        corrected_interest = interest_rate
        monthly_payment = (loan_amount * (1 + corrected_interest/100)**(tenure/12)) / tenure

        # If not eligible, return rejection
        if not approval:
            return Response({"approval": False, "reason": reason}, status=status.HTTP_200_OK)

        # Create new Loan
        loan = Loan.objects.create(
            customer=customer,
            loan_amount=loan_amount,
            tenure=tenure,
            interest_rate=corrected_interest,
            monthly_payment=monthly_payment,
            emis_paid_on_time=0,  # New loan
            date_of_approval=datetime.date.today(),
            end_date=datetime.date.today() + datetime.timedelta(days=30 * tenure)
        )

        # Update customer's current debt
        customer.current_debt += Decimal(str(loan_amount))
        customer.save()

        return Response({
            "loanid": loan.loan_id,
            "approval": True,
            "monthly_payment": int(monthly_payment),
            "tenure": tenure,
            "end_date": loan.end_date.strftime('%Y-%m-%d')
        }, status=status.HTTP_201_CREATED)
    

    from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ViewLoanDetail(APIView):
    def get(self, request, loanid):
        try:
            loan = Loan.objects.get(loan_id=loanid)
            customer = loan.customer
            return Response({
                "loanid": loan.loan_id,
                "customerid": customer.customer_id,
                "customername": f"{customer.first_name} {customer.last_name}",
                "amount": float(loan.loan_amount),
                "tenure": loan.tenure,
                "interest_rate": float(loan.interest_rate),
                "monthly_payment": float(loan.monthly_payment),
                "date_of_approval": loan.date_of_approval,
                "end_date": loan.end_date,
                "emis_paid_on_time": loan.emis_paid_on_time
            }, status=status.HTTP_200_OK)
        except Loan.DoesNotExist:
            return Response({"error": "Loan not found"}, status=status.HTTP_404_NOT_FOUND)



class ViewLoansByCustomer(APIView):
    def get(self, request, customerid):
        try:
            customer = Customer.objects.get(customer_id=customerid)
            loans = Loan.objects.filter(customer=customer)
            loans_data = []
            for loan in loans:
                loans_data.append({
                    "loanid": loan.loan_id,
                    "amount": float(loan.loan_amount),
                    "tenure": loan.tenure,
                    "interest_rate": float(loan.interest_rate),
                    "monthly_payment": float(loan.monthly_payment),
                    "date_of_approval": loan.date_of_approval,
                    "end_date": loan.end_date,
                    "emis_paid_on_time": loan.emis_paid_on_time
                })
            return Response({
                "customerid": customer.customer_id,
                "customername": f"{customer.first_name} {customer.last_name}",
                "loans": loans_data
            }, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

