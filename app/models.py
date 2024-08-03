from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profile_avatar/' , null=True,blank=True, verbose_name='Аватарка')
    phone = PhoneNumberField(unique=True, blank=True, null=True, verbose_name='Номер телефона')

    class Meta: 
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
    
    def __str__(self):
        return self.user.username
    
class Friend(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_friend', verbose_name='Пользователь')
    friend = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend', verbose_name='Друг')
    class Meta:
        verbose_name = 'Друг'
        verbose_name_plural = 'Друзья'

    def __str__(self):
        return f"{self.profile.user.username} -> {self.friend.user.username}"



class Message(models.Model):
    chat = models.ForeignKey('Chat', related_name='messages', on_delete=models.CASCADE, verbose_name='Чат')
    sender = models.ForeignKey(Profile, related_name='sent_messages', on_delete=models.CASCADE, verbose_name='Отправитель')
    content = models.TextField(verbose_name='Содержание')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время отправки')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-timestamp']

    def __str__(self):
        return f"Сообщение от {self.sender.username} в {self.timestamp}"

class Chat(models.Model):
    participants = models.ManyToManyField(Profile, related_name='chats', verbose_name='Участники')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
        ordering = ['-updated_at']

class GroupChat(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название группы')
    participants = models.ManyToManyField(Profile, related_name='group_chats', verbose_name='Участники')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Групповой чат'
        verbose_name_plural = 'Групповые чаты'
        ordering = ['-updated_at']

    def __str__(self):
        return self.name
