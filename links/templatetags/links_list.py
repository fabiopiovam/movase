from django.template import Library
from django.core.exceptions import ObjectDoesNotExist

from links.models import Link

register = Library()

@register.assignment_tag
def get_links(category='', limit=200):
    
    try:
        if not category:
            links = Link.objects.all()[:limit]
        else:
            links = Link.objects.filter(category__slug=category)[:limit]
        
    except ObjectDoesNotExist:
        links = None
    
    return links