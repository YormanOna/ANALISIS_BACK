from abc import ABC, abstractmethod
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Interfaz para las estrategias de notificación
class NotificationStrategy(ABC):
    @abstractmethod
    def send(self, title: str, body: str) -> None:
        pass

# Implementación de WebSocket como estrategia
class WebSocketNotification(NotificationStrategy):
    def send(self, title: str, body: str) -> None:
        channel_layer = get_channel_layer()
        try:
            async_to_sync(channel_layer.group_send)(
                "notifications",
                {
                    "type": "send_notification",
                    "message": {
                        "title": title,
                        "body": body,
                    }
                }
            )
        except Exception as e:
            print(f"Error al enviar notificación WebSocket: {e}")

# Implementación por defecto: notificación por email
class EmailNotification(NotificationStrategy):
    def send(self, title: str, body: str) -> None:
        print(f"[Email] {title}\n{body}")

# Servicio de notificaciones con patrón Singleton
class NotificationService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(NotificationService, cls).__new__(cls, *args, **kwargs)
            cls._instance.strategy = WebSocketNotification()  # Ahora usa WebSocket por defecto
        return cls._instance

    def set_strategy(self, strategy: NotificationStrategy) -> None:
        """Permite cambiar la estrategia de notificación sin modificar el código existente."""
        self.strategy = strategy

    def send_notification(self, title: str, body: str) -> None:
        self.strategy.send(title, body)

# Instancia global del Singleton
notification_service = NotificationService()
