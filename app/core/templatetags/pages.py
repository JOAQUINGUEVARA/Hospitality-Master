from django import template
from core.models import Empresa


register = template.Library()

@register.simple_tag
def get_empresa_datos():
    empresa = Empresa.objects.get(id=1)
    return empresa


