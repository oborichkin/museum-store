from django import template
from ..models import Item


register = template.Library()


@register.simple_tag()
def item_amount(current_user):
    if current_user.is_authenticated:
        return len(Item.objects.filter(owner=current_user))
    else:
        return 0
