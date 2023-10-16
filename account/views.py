from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail


def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # exist
        name = request.POST.get('name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        user = User.objects.filter(username=username)  # [<user object 1>]
        if not user:
            if password1 == password2:
                User.objects.create_user(
                    username=username,
                    first_name=name,
                    email=email,
                    password=password2
                )
                messages.success(request, 'Account created successfully ')
                return redirect('login')
            else:
                messages.error(request, 'Password doesn\'t match !!')
        messages.error(request, 'Username already exist !!')
    return render(request, 'account/register.html')


def user_login(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')

        user = authenticate(username=u, password=p)
        if user:
            login(request, user)
            return redirect('home_page')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'account/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')  # 123
        password2 = request.POST.get('password2')

        users = User.objects.filter(
            username=username)  # []    users = [<User object>] -> user = <User object>       users = User.objects.filter(username=username) # []    []

        if users:
            user = users.first()

            sub = 'Password Reset'
            message = 'Here is your One Time Password(OTP) - 123123'
            from_email = 'safuvansappus@gmail.com'
            to_email = [user.email]

            send_mail(
                subject=sub,
                message=message,
                from_email=from_email,
                recipient_list=to_email,
                fail_silently=False
            )
            # if password1 == password2:
            #     user = users.first()
            #     user.set_password(password2)
            #     user.save()
            messages.success(request, 'Password changed successfully ')
            return redirect('login')
            # else:
            #     messages.error(request, 'Password doesn\'t match !!')
        else:
            messages.error(request, "Username doesn't exist !!! ")

    return render(request, 'account/forgot.html')


def verify_otp(request, id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        submitted_otp = request.POST.get("otp")
        user_otp = UserOTP.object.filter(user=user).first()

        if submitted_otp == user_otp.otp:
            messages.success(request, "OTP verified.")
            return redirect("change_password", user.id)
        messages.error(request, "Invalid OTP....")
    return render(request, "account/verify.otp.html")


def password_reset(request, id):
    user = User.object.get(id=id)
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            user.set_password(password2)
            user.save()
            messages.success(request, 'Password changed successfully')
            return redirect('login')
        messages.error(request, 'Password does not match')

    return render(request, "account/reset.html")
