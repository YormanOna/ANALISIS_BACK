from django.contrib import admin
from .models import Coctail, Paquetes, Clientes, CuentaCliente, Reserva

# Register your models here.
admin.site.register(Coctail)
admin.site.register(Paquetes)
admin.site.register(Clientes)
admin.site.register(CuentaCliente)
admin.site.register(Reserva)