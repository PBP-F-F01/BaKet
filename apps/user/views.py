from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core import serializers
from .models import UserProfile
from django.contrib.auth.models import User

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
@csrf_exempt
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

@login_required
def show_json(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user = User.objects.get(id=request.user.id)
    
    profile_picture = user_profile.profile_picture.url if user_profile.profile_picture else None
    user_json = {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "birth_date": user_profile.birth_date,
        "gender": user_profile.gender,
        "email": user_profile.email,
        "phone_number": user_profile.phone_number,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
        "profile_picture": profile_picture,
    }
    
    # return HttpResponse(serializers.serialize("json", user_json), content_type="application/json")
    return JsonResponse(user_json, content_type="application/json")

@login_required
@csrf_exempt
def update_name_api(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        
        return JsonResponse({'status': 'success', 'message': 'Name updated successfully'}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
@csrf_exempt
def update_birth_date_api(request):
    if request.method == 'POST':
        birth_date = request.POST.get('birth_date')
        
        user_profile = request.user.userprofile
        user_profile.birth_date = birth_date  # Make sure this matches your field format, typically YYYY-MM-DD
        user_profile.save()
        
        return JsonResponse({'status': 'success', 'message': 'Birth date updated successfully'}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
@csrf_exempt
def update_gender_api(request):
    if request.method == 'POST':
        gender = request.POST.get('gender')
        
        user_profile = request.user.userprofile
        user_profile.gender = gender
        user_profile.save()
        
        return JsonResponse({'status': 'success', 'message': 'Gender updated successfully'}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
@csrf_exempt
def update_email_api(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        user_profile = request.user.userprofile
        user_profile.email = email
        user_profile.save()
        
        return JsonResponse({'status': 'success', 'message': 'Email updated successfully'}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
@csrf_exempt
def update_phone_api(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        
        user_profile = request.user.userprofile
        user_profile.phone_number = phone_number
        user_profile.save()
        
        return JsonResponse({'status': 'success', 'message': 'Phone number updated successfully'}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

