
from django.shortcuts import render , redirect,get_object_or_404
from .forms import  FriendRequestForm , CustomUserCreationForm
from .models import Friend , Chat, Message , Profile 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login , authenticate , logout
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



def index(request):
    profile = Profile.objects.get(user=request.user)
    friends = Friend.objects.filter(profile=profile)
    context = {"friends" : friends}
    return render(request, 'index.html' , context)

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


def chat_history(request, friend_id):
    if request.method == 'GET':
        messages = Message.objects.filter(
            sender=request.user, receiver_id=friend_id
        ) | Message.objects.filter(
            sender_id=friend_id, receiver=request.user
        ).order_by('timestamp')

        messages_data = [
            {
                'content': msg.content,
                'file': msg.file.url if msg.file else None,
                'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'is_sender': msg.sender == request.user,
            }
            for msg in messages
        ]

        return JsonResponse({'messages': messages_data})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def send_message(request, friend_id):
    if request.method == 'POST':
        user = request.user
        friend = get_object_or_404(User, id=friend_id)
        content = request.POST.get('content')
        file = request.FILES.get('file')

        if content or file:
            message = Message.objects.create(
                sender=user,
                receiver=friend,
                content=content,
                file=file,
                timestamp=timezone.now()
            )
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def profile_detail(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    data = {
        'username': profile.user.username,
        'avatar': profile.avatar.url if profile.avatar else 'https://abrakadabra.fun/uploads/posts/2021-12/1640528661_1-abrakadabra-fun-p-serii-chelovek-na-avu-1.png',
        'phone': profile.phone or 'Not provided'
    }
    return JsonResponse(data)

