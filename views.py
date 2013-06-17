from django.utils import simplejson
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponseBadRequest, \
    HttpResponse
from django.template import RequestContext
import lib

def callback(request):
    method = request.META['REQUEST_METHOD']
    if method == 'GET':
        return HttpResponse('WHATCHU LOOKIN AT?!')
    elif method == 'POST':
        json_data = simplejson.loads(request.raw_post_data)
        try:
            text = json_data['text']
            if lib.is_cmd(text):
                payload = lib.execcmd(text)
                print payload
                if 'result' in payload:
                    lib.post_chat(payload['result'])
        except KeyError:
            return HttpResponseBadRequest('Malformed data!')
    return HttpResponse(request)
