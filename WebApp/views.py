from django.shortcuts import render

import razorpay
from .models import Chai

from django.views.decorators.csrf import csrf_exempt

from django.conf import settings

from django.core.mail import send_mail
from django.template.loader import render_to_string

# Create your views here.


def home(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        amount = int(request.POST.get("amount")) * 100
        client = razorpay.Client(auth = ("rzp_test_ihdu43wqO3rikQ" , "HNlFCup8cjnyun7Y1Xe0eAr7"))
        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        #print(payment)
        chai = Chai(name = name, email = email, amount = amount, payment_id = payment['id'])
        chai.save()
        return render(request , "home.html" , {'payment' : payment})

    return render(request, "home.html")

@csrf_exempt
def success(request):
    if request.method == "POST":
        a = request.POST
        order_id = ""
        data = {}
        for key , val in a.items():
            if key ==  'razorpay_order_id':
                data['razorpay_order_id'] = val
                order_id = val
            elif key == 'razorpay_payment_id':
                data['razorpay_payment_id'] = val
            elif key == 'razorpay_signature':
                data['razorpay_signature'] = val
        user = Chai.objects.filter(payment_id = order_id).first()
        
        client = razorpay.Client(auth = ("rzp_test_ihdu43wqO3rikQ" , "HNlFCup8cjnyun7Y1Xe0eAr7"))
        check = client.utility.verify_payment_signature(data)

        if check:
            return render(request , "error.html")
        
        user.paid = True
        user.save()

        msg_plain = render_to_string('email.txt')
        msg_html = render_to_string('email.html')


        send_mail("Your amount has been received", msg_plain, settings.EMAIL_HOST_USER , [user.email] , html_message = msg_html)

        
    return render(request, "success.html")