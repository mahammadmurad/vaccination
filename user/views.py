from django.shortcuts import render
from django.urls import reverse
from user.forms import SignupForm, LoginForm, ChangePasswordForm, ProfileUpdateForm
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth import authenticate, login as user_login, logout as user_logout, update_session_auth_hash
from user.email import send_email_verification
from django.contrib.auth import get_user_model
from user.utils import EmailVerificationTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

User = get_user_model()

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return HttpResponseRedirect(reverse('index'))
        messages.error(request, 'Please enter valid data!')
        return render(request, "user/signup.html", {"form": form})
    contex = {
        'form': SignupForm()
        }

    return render(request, 'user/signup.html', contex)


def login(request):
    if request.method=='POST':
        form = LoginForm(request,request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                user_login(request, user)
                messages.success(request,'Login successful')
                return HttpResponseRedirect(reverse('index'))
            messages.error(request,'Please enter valid data!')
            return HttpResponseRedirect(reverse("user:login"))
        messages.error(request, "Please enter valid data!")
        return HttpResponseRedirect(reverse('user:login'))

    context = {
        'form': LoginForm()
    }
    return render(request, 'user/login.html',context)


def logout(request):
    user_logout(request)
    messages.info(request, 'Logout Successfully')
    return HttpResponseRedirect(reverse("user:login"))


def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Change Password Successfully')
            return HttpResponseRedirect(reverse('index'))
        messages.error(request, 'Change Password Failed')
        return render(request, "user/change_password.html", {'form': form})
    context = {
        'form': ChangePasswordForm(request.user)
    }
    return render(request, 'user/change_password.html',context)


def profile_view(request): 
    context = {
        'user': request.user
    }
    
    return render(request, 'user/profile_view.html', context)


def profile_update(request):
    if request.method=='POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return HttpResponseRedirect(reverse('user:profile_view'))
        messages.error(request,'Please enter valid data!')
        return render(request, "user/profile_update.html", {'form': form})
    context = {
        'form': ProfileUpdateForm(instance=request.user)
    }

    return render(request, 'user/profile_update.html', context)


def email_verification_request(request):
    if not request.user.is_email_verified:
        send_email_verification(request, request.user.id)
        return HttpResponse('Email verification link sent to your email address')
    return HttpResponseForbidden('EMail already verified')

def email_verifier(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid) 
    except:
        user = None

    if user == request.user:
        if EmailVerificationTokenGenerator.check_token(user, token):
            user.is_email_verified = True
            user.save() 
            messages.success(request, 'Email verified')
            return HttpResponseRedirect(reverse("user:profile_view"))
        return HttpResponseBadRequest('Invalid request')
    return HttpResponseForbidden("You dont have permission to user this link")
