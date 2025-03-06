# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Coctail
from .services.notification_service import notification_service  # Importar el Singleton

@receiver(post_save, sender=Coctail)
def notify_coctail_change(sender, instance, created, **kwargs):
    if created:
        title = f"Nuevo cóctel añadido: {instance.nombre}"
        body = f"Se ha añadido un nuevo cóctel:\n\nNombre: {instance.nombre}\nPrecio: {instance.precio}"
    else:
        title = f"Cóctel actualizado: {instance.nombre}"
        body = f"El cóctel '{instance.nombre}' ha sido actualizado.\nNuevo Precio: {instance.precio}\nNueva Cantidad: {instance.cantidad}"

    # Usar el Singleton para enviar la notificación
    notification_service.send_notification(title, body)

@receiver(post_delete, sender=Coctail)
def notify_coctail_delete(sender, instance, **kwargs):
    title = f"Cóctel eliminado: {instance.nombre}"
    body = f"El cóctel '{instance.nombre}' ha sido eliminado del sistema."

    # Usar el Singleton para enviar la notificación
    notification_service.send_notification(title, body)