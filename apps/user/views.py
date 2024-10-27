from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile

# Create your views here.
def settings_view(request):
    context = {
    }

    return render(request, 'settings.html', context)

@login_required
@csrf_exempt
def upload_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.profile_picture = request.FILES['profile_picture']
        user_profile.save()
        return JsonResponse({'profile_picture_url': user_profile.profile_picture.url}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def update_name(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        # Update user's first and last name
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        
        messages.success(request, "Name updated successfully.")
        # return redirect('settings')  # Redirect back to settings page (adjust the name if different)
    return redirect('settings_view')

@login_required
def update_birth_date(request):
    if request.method == 'POST':
        birth_date = request.POST.get('birth_date')
        
        # Update birth_date in UserProfile
        user_profile = request.user.userprofile
        user_profile.birth_date = birth_date
        user_profile.save()
        
        messages.success(request, "Birth date updated successfully.")
    return redirect('settings_view')

@login_required
def update_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Update email in UserProfile
        user_profile = request.user.userprofile
        user_profile.email = email
        user_profile.save()
        
        messages.success(request, "Email updated successfully.")
    return redirect('settings_view')

@login_required
def update_phone(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        
        # Update phone number in UserProfile
        user_profile = request.user.userprofile
        user_profile.phone_number = phone_number
        user_profile.save()
        
        messages.success(request, "Phone number updated successfully.")
    return redirect('settings_view')

@login_required
def update_gender(request):
    if request.method == 'POST':
        gender = request.POST.get('gender')
        
        # Update the user's profile gender
        profile = UserProfile.objects.get(user=request.user)
        profile.gender = gender
        profile.save()
        
        # Feedback message (optional)
        messages.success(request, "Your gender has been updated successfully.")
    
    return redirect('settings_view')  # Redirect back to the settings page