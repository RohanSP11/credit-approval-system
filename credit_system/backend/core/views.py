from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Customer, Loan

@csrf_exempt
def register_customer(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        Customer.objects.create(
            name=data['name'],
            gender=data['gender'],
            dob=data['dob'],
            address=data['address'],
            phone=data['phone'],
            email=data['email']
        )
        return JsonResponse({"message": "Customer registered successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=405)

def get_customers(request):
    if request.method == 'GET':
        customers = Customer.objects.all().values()
        return JsonResponse(list(customers), safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def list_customers(request):
    if request.method == 'GET':
        customers = list(Customer.objects.all().values())
        return JsonResponse(customers, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def request_loan(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        try:
            customer = Customer.objects.get(id=data['customer_id'])
            loan = Loan.objects.create(
                customer=customer,
                amount=data['amount'],
                term=data['term'],
                interest_rate=data.get('interest_rate', 10.0)
            )
            return JsonResponse({"message": "Loan requested successfully", "loan_id": loan.id})
        except Customer.DoesNotExist:
            return JsonResponse({"error": "Customer not found"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def loan_status(request, loan_id):
    if request.method == 'GET':
        try:
            loan = Loan.objects.get(id=loan_id)
            return JsonResponse({
                "loan_id": loan.id,
                "customer": loan.customer.name,
                "amount": loan.amount,
                "term": loan.term,
                "interest_rate": loan.interest_rate,
                "status": loan.status
            })
        except Loan.DoesNotExist:
            return JsonResponse({"error": "Loan not found"}, status=404)
