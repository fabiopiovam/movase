from django.template import Library
from django.core.exceptions import ObjectDoesNotExist

from cms.models import Category, Page

register = Library()

@register.inclusion_tag('cms/_list_pages.html')
def list_pages(category='', limit=10):
    
    try:
        if not category:
            pages = Page.activated.all()[:limit]
        else:
            pages = Page.activated.filter(category__slug=category)[:limit]
        
    except ObjectDoesNotExist:
        pages = None
    
    return {'pages': pages,}

@register.assignment_tag
def get_page_links(category='', limit=20):
    
    try:
        if not category:
            pages = Page.activated.all()[:limit]
        else:
            pages = Page.activated.filter(category__slug=category)[:limit]
        
    except ObjectDoesNotExist:
        pages = None
    
    return pages