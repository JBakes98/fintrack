from django.shortcuts import render


def index(request):
    return render(request, 'fintrack_fe/index.html')