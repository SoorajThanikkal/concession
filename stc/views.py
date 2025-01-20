from django.shortcuts import render,redirect
from stc import models
from django.shortcuts import render 
import razorpay
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.conf import settings
# from razorpay.errors import BadRequestError
from django.views.decorators.csrf import csrf_exempt
def logout(request):
    request.session.flush()
    return redirect('login')

# Create your views here.
def index_view(request):
    if 'email' not in request.session:
        return redirect('login') 
    else:
        try:
            email=request.session['email']
            student = models.user.objects.get(email=email)
            return render(request,'index.html',{'student':student})
        except:
            return redirect('login')

def just(request):
    return render(request,'just.html')

def cindex(request):
    if 'bemail' in request.session:
        email = request.session['bemail']
        try:
            book = models.BusConductor.objects.get(email=email)
            print(book)
            return render(request,'cindex.html',{'book':book})
        except:
            alert="<script>alert('You are not loggined!'); window.location.href='/login/';</script>"
            return HttpResponse(alert)
    else:
        alert="<script>alert('You are not loggined!'); window.location.href='/login/';</script>"
        return HttpResponse(alert)
def locations(request): 
    return render(request, 'locations.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        photo = request.FILES.get('photo')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        phonenumber = request.POST.get('phonenumber')

        # Create the user object
        obj =models.user(name=name, email=email, password=password, image=photo, gender=gender, dob=dob, phonenumber=phonenumber)
        obj.save()

        # Set session variable to indicate user is logged in
        request.session['email'] = email  # or use obj.id if preferred

        # Redirect to the index page after registration
        return redirect('login')

    # Render the signup page if method is GET
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Check if the user is a regular user
            us = models.user.objects.get(email=email, password=password)
            semail = us.email
            request.session['email'] = semail
            return redirect('index')
        except models.user.DoesNotExist:
            # If not a regular user, check if the user is a conductor
            try:
                us = models.BusConductor.objects.get(email=email, password=password)
                semail = us.email
                request.session['bemail'] = semail
                return redirect('cindex')
            except models.BusConductor.DoesNotExist:
                # If neither, return an invalid entry message
                msg = "Invalid credentials. Please try again."
                return render(request, 'login.html', {"msg": msg})

    return render(request, "login.html")

def profile(request):
    if 'email' in request.session:
        email=request.session['email']
        usr=models.user.objects.get(email=email)
    return render(request,"profile.html",{'usr':usr})

def edit(request, uid):
    edit = models.user.objects.get(id=uid)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        photo = request.FILES.get('image')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        phonenumber = request.POST.get('phonenumber')
        from_address = request.POST.get('from_address')
        to_address = request.POST.get('to_address')
        
        edit.name = username
        edit.email = email
        edit.dob = dob
        edit.gender = gender
        edit.phonenumber = phonenumber
        edit.from_address = from_address
        edit.to_address  = to_address
        if photo is not None:
            edit.image = photo
        
        edit.save()
        return redirect('profile')
    return render(request, 'edit.html', {'edit': edit})
def ShowWallet(request):
    if 'email' in request.session:
        email= request.session['email']
        try:
            usr= models.user.objects.get(email=email)
        except:
            return redirect('login')
        wlt=models.Wallet.objects.filter(wuser=usr)

        return render(request,'showmywallet.html',{'wlt':wlt})
    return redirect('login')

def initiate_payment(request,amount):
    email = request.session['email']
    if email:
        amount = int(amount)*100 
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        payment_order = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        order_id = payment_order['id']
        user = models.user.objects.get(email=email)
        buyer_data = {
            'buyer': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'phone': user.phonenumber,
                # Add other fields as needed
            }
        }
        response_data = {'order_id': order_id, 'amount': amount}
        response_data.update(buyer_data)
        return JsonResponse(response_data, encoder=DjangoJSONEncoder)
    else:
        return redirect('login')
from decimal import Decimal   
@csrf_exempt
def confirm_payment(request, order_id, payment_id):
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    try:
        payment = client.payment.fetch(payment_id)
        print('payment', payment)
        if payment['order_id'] == order_id and payment['status'] == 'captured':
            pemail = payment.get('email')
            amount = payment.get('amount')
            amount_in_rupees = Decimal(amount) / Decimal(100)  # Convert to rupees

            if pemail:
                usr = models.user.objects.get(email=pemail)
                wallet, created = models.Wallet.objects.get_or_create(wuser=usr, defaults={'amount': 0})

                if not created:  
                    wallet.amount += amount_in_rupees
                else: 
                    wallet.amount = amount_in_rupees
                    wallet.is_paid=True

                wallet.save()
                return redirect('index')
            else:
                return JsonResponse({'status': 'failure', 'error': 'User email not found'})
    except Exception as e:
        print('Error:', str(e))
        return redirect('index')
    
from .models import BusPass, BusRoute, user,Transaction,Wallet

def book_bus_pass(request):
    if request.method == "POST":
        # Retrieve the user object from the session or database
        email = request.session.get('email')  # Assuming email is stored in the session
        try:
            user_obj = user.objects.get(email=email)
        except user.DoesNotExist:
            return JsonResponse({'error': 'User not found. Please login again.'}, status=404)

        # Check if the user already has an active pass
        if BusPass.objects.filter(user=user_obj, is_paid=True).exists():
            return JsonResponse({'error': 'You already have an active bus pass.'}, status=400)

        # Get `from_address` and `to_address` from the request
        from_address = request.POST.get('from_address')
        to_address = request.POST.get('to_address')

        # Find the bus route and calculate fare
        try:
            route = BusRoute.objects.get(start_point=from_address, end_point=to_address)
        except BusRoute.DoesNotExist:
            return JsonResponse({'error': 'Route not found. Please select a valid route.'}, status=404)

        fare = route.fare

        # Create a bus pass without deducting the wallet balance
        bus_pass = BusPass(
            user=user_obj,
            from_address=from_address,
            to_address=to_address,
            amount=fare,
            is_paid=True
        )
        bus_pass.generate_qr_code()
        bus_pass.save()

        alert = "<script>alert('Bus Pass Booked SuccesFully'); window.location.href='/book_bus/';</script>"
        return HttpResponse(alert)

    # Render the booking form for GET requests
    email = request.session.get('email')  # Assuming email is stored in the session
    try:
        user_obj = user.objects.get(email=email)
    except user.DoesNotExist:
        return JsonResponse({'error': 'User not found. Please login again.'}, status=404)
    
    # Check for an active pass
    active_pass = BusPass.objects.filter(user=user_obj, is_paid=True).first()
    
    return render(request, 'book_bus.html', {
        'user_obj': user_obj,
        'active_pass': active_pass  # Pass active pass info to the template
    })


def parse_qr_data(qr_data):
    """
    Parses the QR code data string and extracts the user email, 
    from_address, to_address, and amount.

    Args:
        qr_data (str): The string data from the QR code.

    Returns:
        tuple: (user_email, from_address, to_address, amount)
    """
    try:
        # Split the data string into components
        data_parts = qr_data.split(", ")
        
        # Extract specific details
        user_email = data_parts[0].split(": ")[1]
        from_address = data_parts[1].split(": ")[1]
        to_address = data_parts[2].split(": ")[1]
        amount = float(data_parts[3].split(": ")[1])  # Convert amount to float
        
        return user_email, from_address, to_address, amount
    except Exception as e:
        raise ValueError(f"Error parsing QR data: {str(e)}")

from django.shortcuts import render
from django.http import JsonResponse
from .models import BusPass, BusConductor, Transaction


def scan_qr_code(request):
    if request.method == "POST":
        # Process the scanned QR code data
        qr_data = request.POST.get('qr_data')  # Extracted from QR scanner

        # Parse the QR code data
        try:
            user_email, from_address, to_address, amount = parse_qr_data(qr_data)
        except ValueError as e:
            return JsonResponse({'error': f'Invalid QR code data: {str(e)}'}, status=400)

        # Verify the bus pass
        try:
            bus_pass = BusPass.objects.get(
                user__email=user_email, from_address=from_address,
                to_address=to_address, amount=amount, is_paid=True
            )
        except BusPass.DoesNotExist:
            alert = "<script>alert('Invalid or expired bus pass'); window.location.href='/scan-qr/';</script>"
            return HttpResponse(alert)

        # Check if the bus pass can still be used
        if bus_pass.usage_count >= bus_pass.max_usage:
            alert = "<script>alert('Bus pass has been used the maximum number of times today.'); window.location.href='/scan-qr/';</script>"
            return HttpResponse(alert)

        # Check if the conductor is logged in
        try:
            conductor_email = request.session.get('bemail')  # Assuming conductor email is in the session
            conductor = BusConductor.objects.get(email=conductor_email)
        except BusConductor.DoesNotExist:
            alert = "<script>alert('Please login'); window.location.href='/login/';</script>"
            return HttpResponse(alert)

        # Retrieve wallet associated with the user
        try:
            wallet = Wallet.objects.get(wuser=bus_pass.user)
        except Wallet.DoesNotExist:
            alert = "<script>alert('Wallet not found for the user'); window.location.href='/scan-qr/';</script>"
            return HttpResponse(alert)

        # Check if the wallet has sufficient balance
        if wallet.amount < bus_pass.amount:
            alert = "<script>alert('Insufficient wallet balance'); window.location.href='/scan-qr/';</script>"
            return HttpResponse(alert)

        # Deduct fare from the wallet
        wallet.amount -= bus_pass.amount
        wallet.save()

        # Record the transaction and increment the usage count
        Transaction.objects.create(bus_pass=bus_pass, conductor=conductor, amount=bus_pass.amount)
        bus_pass.usage_count += 1  # Increment usage count
        bus_pass.save()

        # Return success response
        alert = "<script>alert('Bus pass validated successfully!'); window.location.href='/scan-qr/';</script>"
        return HttpResponse(alert)

    # Handle GET request to render the QR code scanning page
    elif request.method == "GET":
        return render(request, 'scan_qr.html')

    return JsonResponse({'error': 'Invalid request method'}, status=400)



def adminlogin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        u='vinu'
        p='121212'
        if username==u:
            if password==p:
                return redirect('adminhome')
    return render(request,'adminlogin.html')

def adminhome(request):
    return render(request,'adminhome.html')

def user_list(request):
    users = models.user.objects.all() 
    return render(request, 'userlist.html', {'users':users})

def delete_userlist(request,did):
    x=models.user.objects.get(id=did)
    x.delete()
    return redirect('userlist')

from django.http import HttpResponse
from django.shortcuts import render
from .models import Feedback  # Assuming Feedback model is imported

def feedback(request):
    if request.method == "POST":
        feedback_text = request.POST.get('feedback_text')
        rating = request.POST.get('rating')
        email = request.POST.get('email')

        # Handle missing fields
        if not feedback_text or not rating:
            alert_message = "<script>alert('Please fill in all required fields.'); window.location.href='/feedback_rate';</script>"
            return HttpResponse(alert_message)

        try:
            rating = int(rating)
            if rating not in [1, 2, 3, 4, 5]:
                raise ValueError("Invalid rating value")
        except (ValueError, TypeError):
            # Handle invalid rating
            alert_message = "<script>alert('Invalid rating value. Please select a valid rating.'); window.location.href='/feedback_rate';</script>"
            return HttpResponse(alert_message)

        # Create and save the Feedback instance
        feedback_instance = Feedback(
            feedback_text=feedback_text,
            rating=rating,email=email
        )
        feedback_instance.save()

        # Success message with JavaScript
        success_message = "<script>alert('Feedback submitted successfully!'); window.location.href='/feedback_rate';</script>"
        return HttpResponse(success_message)

    # Render the feedback form for GET requests
    return render(request, 'feedback_rate.html')


def set_locations(request):
    if request.method == 'POST':
        from_address = request.POST.get('from_address')
        to_address = request.POST.get('to_address')
        # Save the addresses in the user's profile
        profile.from_address = from_address
        profile.to_address = to_address
        profile.save()
        return redirect('profile')  # Redirect to the profile view after saving
    return render(request, 'locations.html', {'profile': profile})


#conductor section
def conductorRegister(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        busname = request.POST.get('busname')
        photo = request.FILES.get('photo')

        # Check if the email already exists in the `user` model or `rto` model
        if models.user.objects.filter(email=email).exists() or models.rto.objects.filter(email=email).exists():
            alert = "<script>alert('User already exists with this email'); window.location.href='/conductorRegister/';</script>"
            return HttpResponse(alert)

        # Save the conductor data
        cd = models.BusConductor(name=name, email=email, password=password, busname=busname, photo=photo)
        cd.save()

        return redirect('login')

    return render(request, 'conductorreg.html')


def conductorprofile(request):
    if 'bemail' in request.session:
        bemail= request.session['bemail']
        try:
            cd = models.BusConductor.objects.get(email=bemail)
            return render(request, 'conductorprofile.html', {'cd': cd})
        except BusConductor.DoesNotExist:
            alert="<script>alert('You are not loggined!'); window.location.href='/login/';</script>"
            return HttpResponse(alert)
    alert="<script>alert('You are not loggined!'); window.location.href='/login/';</script>"
    return HttpResponse(alert)
    
    


