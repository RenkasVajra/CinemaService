from django import template
from django.utils.translation import gettext_lazy as _


register = template.Library()


@register.filter
def mul(value, arg):
    return value * arg


@register.filter
def month_name(month_num):
    """Возвращает название месяца в нужном падеже."""
    months = {
        'Январь': _("Января"),
        'Февраль': _("Февраля"),
        'Март': _("Марта"),
        'Апрель': _("Апреля"),
        'Май': _("Мая"),
        'Июнь': _("Июня"),
        'Июль': _("Июля"),
        'Август': _("Августа"),
        'Сентябрь': _("Сентября"),
        'Октябрь': _("Октября"),
        'Ноябрь': _("Ноября"),
        'Декабря': _("Декабря"),
    }
    return months.get(month_num, '')