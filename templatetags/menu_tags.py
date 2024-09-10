from django import template
from django.utils.safestring import mark_safe
from ..models import Menu, MenuItem

register = template.Library()

@register.simple_tag
def draw_menu(menu_name):
    try:
        menu = Menu.objects.get(name=menu_name)
    except Menu.DoesNotExist:
        return mark_safe('')

    items = menu.items.filter(parent__isnull=True)
    return mark_safe(render_menu(items))

def render_menu(items):
    html = '<ul>'
    for item in items:
        html += f'<li><a href="{item.get_url()}">{item.title}</a>'
        children = item.children.all()
        if children.exists():
            html += render_menu(children)
        html += '</li>'
    html += '</ul>'
    return html
