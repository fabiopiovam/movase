from django.template import Library
from django.core.exceptions import ObjectDoesNotExist

from cms.models import Category, Page

register = Library()

@register.inclusion_tag('cms/_list_pages.html')
def list_pages(category='', limit=10, orderby='id', section='main'):
    #TODO: verificar orderby
    try:
        if not category:
            pages = Page.activated.all().order_by(orderby)[:limit]
        else:
            pages = Page.activated.filter(category__slug=category).order_by(orderby)[:limit]
        
    except ObjectDoesNotExist:
        pages = None
    
    page_section = "cms/_list_pages_%s.html" % section
    
    return {'pages': pages, 'page_section': page_section}

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

@register.assignment_tag
def get_categories(object=None, limit=20):
    
    try:
        if not object:
            categories = Category.objects.all()[:limit]
        else:
            categories = object.category_set.all()[:limit]
        
    except ObjectDoesNotExist:
        categories = None
    
    return categories