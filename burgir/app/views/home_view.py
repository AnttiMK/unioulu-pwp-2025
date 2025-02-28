from django.shortcuts import render


def home(request):
    """
    Home page for django admin panel
    """
    return render(request, "home.html")
