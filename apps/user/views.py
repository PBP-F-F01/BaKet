from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
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