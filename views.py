from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponseBadRequest, \
    HttpResponse
from django.template import RequestContext

def callback(request):
    method = request.META['REQUEST_METHOD']
    print method
    print request
    if method == 'GET':
        return HttpResponse('WHATCHU LOOKIN AT?!')
    elif method == 'POST':
        print request.POST
    return HttpResponse(request)
