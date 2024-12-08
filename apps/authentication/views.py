import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date

from apps.user.models import UserProfile

@csrf_exempt
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            # Status login sukses.
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "Login sukses!"
                # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali username atau kata sandi."
        }, status=401)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                "status": False,
                "message": "Invalid JSON."
            }, status=400)
        
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        birth_date_str = data.get('birth_date')  # Expecting format YYYY-MM-DD
        gender = data.get('gender')  # 'Pria' or 'Wanita'

        # Validate required fields
        if not username or not password1 or not password2 or not birth_date_str or not gender:
            return JsonResponse({
                "status": False,
                "message": "Missing required fields."
            }, status=400)
        
        # Check if the passwords match
        if password1 != password2:
            return JsonResponse({
                "status": False,
                "message": "Passwords do not match."
            }, status=400)
        
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": False,
                "message": "Username already exists."
            }, status=400)
        
        # Validate birth_date
        birth_date = parse_date(birth_date_str)
        if not birth_date:
            return JsonResponse({
                "status": False,
                "message": "Invalid birth_date format. Expected YYYY-MM-DD."
            }, status=400)
        
        # Validate gender choice
        if gender not in ['Pria', 'Wanita']:
            return JsonResponse({
                "status": False,
                "message": "Invalid gender. Expected 'Pria' or 'Wanita'."
            }, status=400)
        
        # Create the new user
                # If all validations pass, create user
        user = User.objects.create_user(
            username=username, 
            password=password1, 
            first_name=first_name, 
            last_name=last_name
        )

        # Create user profile
        UserProfile.objects.create(
            user=user,
            birth_date=birth_date,
            gender=gender
        )
        user.save()
        
        return JsonResponse({
            "username": user.username,
            "status": 'success',
            "message": "User created successfully!"
        }, status=200)
    
    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)