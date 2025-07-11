
from django.shortcuts import render
from cocina.models import OrdenProduccion, Receta, Ingrediente
from caja.models import PedidoCaja
from django.db.models import Sum, Count

def dashboard_view(request):
    resumen_pedidos = PedidoCaja.objects.aggregate(
        total_valor=Sum('valor_total'),  # Cambia 'valor_total' por el nombre real del campo de valor
        total_cantidad=Count('id')
    )
    total_valor_pedidos = resumen_pedidos['total_valor'] or 0
    total_cantidad_pedidos = resumen_pedidos['total_cantidad'] or 0

    total_por_mesa = (
    PedidoCaja.objects
    .values('IdMesa')
    .annotate(total_valor=Sum('valor_total'))
    .order_by('IdMesa')
    )

    # Total por habitación
    total_por_habitacion = (
    PedidoCaja.objects
    .values('IdHabitacion')
    .annotate(total_valor=Sum('valor_total'))
    .order_by('IdHabitacion')
    )
   
    context = {
        'total_valor_pedidos': total_valor_pedidos,
        'total_cantidad_pedidos': total_cantidad_pedidos,
        'total_por_mesa': total_por_mesa,
        'total_por_habitacion': total_por_habitacion,
    }
    return render(request, 'dashboard.html', context)