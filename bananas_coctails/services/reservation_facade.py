import logging
from django.db import transaction
from bananas_coctails.models import Reserva  # Reemplaza 'myapp' con el nombre de tu aplicación
from .notification_service import notification_service
import json

logger = logging.getLogger(__name__)

class ReservationFacade:
    """
    Facade para manejar la creación de reservas y el envío de notificaciones.
    """

    def create_reservation(self, servicio, fecha, direccion, cocteles, costo_estimado):
        """
        Crea una reserva y envía una notificación.
        """
        if not servicio or not fecha or not direccion or not cocteles or not costo_estimado:
            raise ValueError("Todos los campos son obligatorios.")
        

        try:
            # Serializar los cocteles a JSON si es necesario
            if isinstance(cocteles, list):
                cocteles = json.dumps(cocteles)

            with transaction.atomic():  # Asegura que la reserva se cree de manera atómica
                reserva = Reserva.objects.create(
                    servicio=servicio,
                    fecha=fecha,
                    direccion=direccion,
                    cocteles=cocteles,
                    costo_estimado=costo_estimado
                )

            # Enviar notificación de manera asíncrona
            logger.info(f"Reserva creada con ID: {reserva.id}")
            logger.debug("Intentando enviar notificación...")
            notification_service.send_notification(
                title="Nueva reserva creada",
                body=f"Se ha creado una reserva para {servicio} en {fecha}."
            )

            return reserva
        except Exception as e:
            logger.error(f"Error al crear la reserva: {e}")
            raise

# Instancia reutilizable del Facade
reservation_facade = ReservationFacade()
