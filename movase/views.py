# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist

from carousel.models import Carousel

def index(request):    
    template = loader.get_template('movase/index.html')
    context = RequestContext(request, {
        'msg'  : 'hola!',
    })
    
    return HttpResponse(template.render(context))