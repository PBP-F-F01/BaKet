from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse

def index(request):
    context = {
        'current_time': datetime.now(),
    }
    return render(request, "main.html", context)
    