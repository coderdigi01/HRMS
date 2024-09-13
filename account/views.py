from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login , authenticate, logout
from django.contrib import messages
from django.http import JsonResponse
from .models import UserProfile
import random
from .models import OTP
import datetime

# def loginView(request):
#     return render(request, 'account/login.html.j2')



def send_otp(mobile_number):
    # mobile_number = request.POST.get('mobile_number')
    try:
        user = UserProfile.objects.get(mobile_number=mobile_number)
        otp_code = str(random.randint(100000, 999999))  # Generate 6-digit OTP
        OTP.objects.create(user=user, otp=otp_code)
        
        # Send OTP to user via SMS (you can use an SMS service here)
        # For example: send_sms(user.mobile_number, otp_code)
        
        return JsonResponse({'success': True, 'message': 'OTP sent successfully'})
    except UserProfile.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'User not found'})

# Validate OTP
def validate_otp(request, mobile_number, otp_code):
    # mobile_number = request.POST.get('mobile_number')
    # otp_code = request.POST.get('otp')

    try:
        user = UserProfile.objects.get(mobile_number=mobile_number)
        otp_record = OTP.objects.filter(user=user).latest('created_at')

        # Check if OTP matches and is valid (e.g., OTP valid for 5 minutes)
        if otp_record.otp == otp_code: #and otp_record.created_at > datetime.datetime.now() - datetime.timedelta(minutes=5):
            auth_login(request, user)
            otp_record.delete()  # Delete OTP after successful validation
            return JsonResponse({'success': True, 'message': 'OTP validated successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid or expired OTP'})

    except (UserProfile.DoesNotExist, OTP.DoesNotExist):
        return JsonResponse({'success': False, 'message': 'OTP or user not found'})


# User Signup View
def user_signup(request):
    if request.method == 'POST':
        mobile_number = request.POST.get('mobile_number')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not UserProfile.objects.filter(mobile_number=mobile_number).exists():
            user = UserProfile.objects.create(mobile_number=mobile_number, password=password, email=email)
            messages.success(request, 'User registered successfully.')
            return redirect('login')
        else:
            messages.error(request, 'Mobile number is already registered.')

    return render(request, 'account/signup.html.j2')

# OTP Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('mobile_number')
        password = request.POST.get('password')
        if not username and not password:
                messages.error(request, 'Your username or password is not valid')
                return redirect('/')
        else:
            user = authenticate(mobile_number=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')
            else:
                user_object = UserProfile.objects.filter(mobile_number=username)
                if user_object.exists():
                    messages.error(request, 'Your password is incorrect')
                else:
                    messages.error(request, 'Your username is incorrect')
                return redirect('login')
        #get_otp = request.POST.get('send_otp')
        #verify_otp = request.POST.get('otp')

        # Simulate sending OTP
        # if get_otp == '1':
        #     # Your logic to send OTP here
        #     otp_sent = send_otp(mobile_number)
        #     # Example: OTP sent successfully
        #     otp_sent = True  # Simulate OTP sending success
        #     if otp_sent:
        #         return JsonResponse({'otp': True})  # OTP was sent
        #     else:
        #         return JsonResponse({'otp': False})  # OTP sending failed
        # if verify_otp:    
        #     verified = validate_otp(request, mobile_number, verify_otp)

        # if 'get_otp' in request.POST:
        #     generated_otp = str(random.randint(100000, 999999))
        #     OTP.objects.create(user=request.user, otp=generated_otp)
        #     return JsonResponse({'message': 'OTP sent successfully', 'otp': generated_otp})

        # if 'verify_otp' in request.POST:
        #     store_otp = OTP.objects.get(user=request.user)
        #     if store_otp.otp == get_otp:
        #         user = authenticate(mobile_number=mobile_number)
        #         if user:
        #             login(request, user)
        #             return redirect('dashboard')
        #     return JsonResponse({'error': 'Invalid OTP'})

    return render(request, 'index.html.j2')

def forgot_password(request):
    if request.method == 'POST':
        data = request.POST
        mobile = data.get('mobile')
        password = data.get('confirm-pin')
        if mobile:
            user = UserProfile.objects.get(mobile_number=mobile)
        else:
            return JsonResponse({'success': False})
        profile = UserProfile.objects.get(user=user)
        profile.password=password
        profile.save()
        if user:
            return redirect('dashboard')
        else:
            return redirect('login')

# User Logout View
def user_logout(request):
    logout(request)
    return redirect('home')
