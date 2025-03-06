from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializer import CoctailSerializer, PaquetesSerializer, ClientesSerializer, CuentaClienteSerializer, ReservaSerializer
from .models import Coctail, Paquetes, Clientes, CuentaCliente, Reserva

from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from bananas_coctails.services.reservation_facade import reservation_facade

# Create your views here.
class CoctailViewSet(viewsets.ModelViewSet):
    queryset = Coctail.objects.all()
    serializer_class = CoctailSerializer

class PaquetesViewSet(viewsets.ModelViewSet):
    queryset = Paquetes.objects.all()
    serializer_class = PaquetesSerializer

class ClientesViewSet(viewsets.ModelViewSet):
    queryset = Clientes.objects.all()
    serializer_class = ClientesSerializer

class CuentaClienteViewSet(viewsets.ModelViewSet):
    queryset = CuentaCliente.objects.all()
    serializer_class = CuentaClienteSerializer

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

    def create(self, request, *args, **kwargs):
        """
        Sobrescribe la creación de una reserva para utilizar el Facade.
        """
        try:
            data = request.data  # Obtener datos de la solicitud
            nueva_reserva = reservation_facade.create_reservation(
                servicio=data["servicio"],
                fecha=data["fecha"],
                direccion=data["direccion"],
                cocteles=data["cocteles"],
                costo_estimado=data["costo_estimado"]
            )

            return Response({
                "mensaje": "Reserva creada exitosamente",
                "id": nueva_reserva.id
            }, status=status.HTTP_201_CREATED)

        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Error interno del servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
def send_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data['email']
            subject = data['subject']
            message = data['message']

            full_message = f"De: {email}\n\nMensaje:\n{message}"

            send_mail(
                subject,
                full_message,
                'onayorman@gmail.com',  
                ['onayorman@gmail.com'],  
                fail_silently=False,
            )
            return JsonResponse({'message': 'Email sent successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid HTTP method'}, status=400)