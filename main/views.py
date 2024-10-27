from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from apps.catalogue.models import Cart
from django.contrib.auth.decorators import login_required
from main.models import UserProfile

def index(request):
    context = {
        'current_time': datetime.now(),
    }
    return render(request, "main.html", context)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create UserProfile if not exist (prevent duplicate)
            profile, created = UserProfile.objects.get_or_create(user=user)
            
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Check if UserProfile exists for this user, create if it doesn't
            UserProfile.objects.get_or_create(user=user)
            
            # Redirect to 'next' URL if available, otherwise go to index
            next_url = request.GET.get('next')
            if next_url:
                return HttpResponseRedirect(next_url)
            else:
                return redirect('main:index')
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:index'))
    response.delete_cookie('last_login')
    return response

@login_required
def get_cart_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_count = cart.cartitem_set.count()

    return JsonResponse({'cart_count': cart_count})