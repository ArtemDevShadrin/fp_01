from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'users/index.html')

def new(request):
    return render(request, 'users/new.html')
