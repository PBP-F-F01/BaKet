from django.shortcuts import render

# Create your views here.
def settings_view(request):
    context = {
    }

    return render(request, 'settings.html', context)
