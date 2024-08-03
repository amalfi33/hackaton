from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Friend, Chat

@receiver(post_save, sender=Friend)
def create_chat_on_friendship(sender, instance, **kwargs):
    profile1 = instance.profile
    profile2 = instance.friend

    # Получаем или создаем чат для двух профилей
    chat = Chat.get_or_create_chat([profile1, profile2])
