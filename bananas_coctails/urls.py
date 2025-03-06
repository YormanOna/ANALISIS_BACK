from django.urls import path, include
from rest_framework import routers
from bananas_coctails import views
from rest_framework.documentation import include_docs_urls
from .views import send_email

router = routers.DefaultRouter()
router.register(r'coctails', views.CoctailViewSet,'coctails')
router.register(r'paquetes', views.PaquetesViewSet,'paquetes')
router.register(r'clientes', views.ClientesViewSet,'clientes')
router.register(r'cuentacliente', views.CuentaClienteViewSet,'cuentacliente')
router.register(r'reservas', views.ReservaViewSet, basename='reserva')

urlpatterns = [
    path('api/info/',include(router.urls)),
    path('docs/', include_docs_urls(title='Bananas Coctails API')),
    path('send-email/', views.send_email, name='send_email'),
]