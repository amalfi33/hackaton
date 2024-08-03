from django.shortcuts import render , redirect,get_object_or_404
from .forms import  FriendRequestForm
from .models import Friend , Chat, Message
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login , authenticate , logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


def index(request):
    return render(request, 'index.html')

# Регистрация и аутентификация 


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {"form": form})



def login_site(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
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

@login_required
def friends_list(request):
    friends = Friend.objects.filter(user=request.user, status='accepted')
    friend_requests = Friend.objects.filter(friend=request.user, status='pending')
    return render(request, 'friends_list.html', {'friends': friends, 'friend_requests': friend_requests})

@login_required
def handle_friend_request(request, friend_request_id, action):
    friend_request = get_object_or_404(Friend, id=friend_request_id)
    if action == 'accept':
        friend_request.status = 'accepted'
        Friend.objects.create(user=friend_request.friend, friend=friend_request.user, status='accepted')
    elif action == 'reject':
        friend_request.status = 'rejected'
    friend_request.save()
    return redirect('friends_list')
