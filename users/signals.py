# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from notifications.models import Notification


from .models import CustomUser, DemandeDemarcheur

@receiver(post_save, sender=CustomUser)
def notify_admin_on_demande_demarcheur(sender, instance, created, **kwargs):
    print("Signal appelé !")  # Debug
    
    if not created and instance.demande_demarcheur:
        print(f"Notification à envoyer pour {instance.full_name}")  # Debug
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "admin_notifications",
            {
                "type": "demande_notification",
                "message": f"L'utilisateur {instance.full_name} a demandé à devenir démarcheur"
            }
        )

    if not created and instance.is_demarcheur:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{instance.id}",
            {
                "type": "promotion_notification",
                "message": "Votre demande pour devenir démarcheur a été acceptée ! 🎉"
            }
        )

@receiver(post_save, sender=DemandeDemarcheur)
def create_notification(sender, instance, created, **kwargs):
    if created:
        # Tu identifies ici l'administrateur ou un superuser
        admin_users = CustomUser.objects.filter(is_superuser=True)
        for admin in admin_users:
            notif = Notification.objects.create(
                recipient=admin,
                message=f"{instance.user.full_name} a fait une demande pour devenir démarcheur.",
                type='demande'
            )

            # Envoi WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'admin_notifications_{admin.id}',
                {
                    'type': 'send_notification',
                    'message': notif.message,
                    'id': notif.id,
                    'type': notif.type,
                }
            )