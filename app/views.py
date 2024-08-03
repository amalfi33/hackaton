from django.shortcuts import render , redirect
from .forms import RegisterForm
from django.contrib.auth import login , authenticate , logout
# Create your views here.
def index(request):
    return render(request, 'index.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user=user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {"form" : form})

def login_site(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request , username=username,password=password)
        if user is not None:
            login(request, user=user)
            return redirect('index')
        else:
            return render(request, 'index.html' , {"error" : "неверное имя или пароль"})
    return render(request, "login.html")

def logout_site(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')
