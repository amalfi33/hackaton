from django.shortcuts import render , redirect,get_object_or_404
from .forms import  FriendRequestForm , CustomUserCreationForm
from .models import Friend , Chat, Message , Profile 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login , authenticate , logout
from django.contrib.auth.models import User



def index(request):
    return render(request, 'index.html')

# Регистрация и аутентификация 
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {"form": form})



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
# ------------------------------------------------------

# Добавление в друзья
@login_required
def send_friend_request(request):
    if request.method == 'POST':
        form = FriendRequestForm(request.POST)
        if form.is_valid():
            friend_request = form.save(commit=False)
            friend_request.user = request.user
            friend_request.save()
            return redirect('friends_list')
    else:
        form = FriendRequestForm()
    return render(request, 'send_friend_request.html', {'form': form})


def index(request):
    # Получите профиль текущего пользователя
    profile = Profile.objects.get(user=request.user)
    
    # Получите список друзей текущего пользователя
    friends = Friend.objects.filter(profile=profile)
    
    # Передайте данные в контекст шаблона
    return render(request, 'index.html', {'friends': friends})
