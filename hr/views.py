from django.shortcuts import render

# Create your views here.

def home(request):
    # return render(request, 'hr/home.html.j2')
    return render(request, 'hr/index.html.j2')


def dashboard(request):
    return render(request, 'hr/dashboard.html.j2')
