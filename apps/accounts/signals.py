from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cliente, Mesero
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def crear_cliente(sender, instance, created, **kwargs):
    if created and instance.user_type == 'cliente':
        Cliente.objects.create(user=instance)