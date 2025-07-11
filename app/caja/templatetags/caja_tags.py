from django import template
from caja.models import SesionCaja,Caja,PedidoCaja


register = template.Library()

@register.simple_tag
def get_sesiones_caja_list():
    sesiones = SesionCaja.objects.filter(abierta=1)
    return sesiones


@register.simple_tag
def get_caja_list():
    cajas =Caja.objects.all()
    return cajas

""" @register.simple_tag
def get_pedidos_total():
    total_pagos =PedidoCaja.objects.filter(cerrado=False).aggregate(Sum('valor_total'))['valor__sum']   """

