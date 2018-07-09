from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
# from __future__ import unicode_literals
# Create your views here.
from .match_api import Match_API
import json
from django.shortcuts import redirect


def Convert(tup, di):
    for a, b, c in tup:
        di.setdefault(a, c)
    return di


@csrf_exempt
def predict(request):
    patentDescription = request.POST.get('patentDescription')
    compno = request.POST.get('compno')
    # compno = request.POST.get('compno')
    print('comp: ', )
    print("predict")
    if request.method == "POST" and request.is_ajax:
        # api = API()
        # result = api.predict(patentDescription)
        # result = result[:5]
        matcher = Match_API()
        result = matcher.getMatches(patentDescription , int(compno))
        print('result',result)
        dictionary = {}
        # result = Convert(result, dictionary)
        context = {
            'data2': result
        }
        context['data2'] = json.dumps(result)
        return HttpResponse(context['data2'])



def index(request):
    context = {}
    # context['data2'] = None
    # patentDescription = request.POST.get('patentDescription')
    template = loader.get_template('index.html')
    # if request.method == 'POST' and patentDescription != None:
    #     print("ssss ", patentDescription)
    #     api = API()
    #     result = api.predict(patentDescription)
    #     result = result[:5]
    #     dictionary = {}
    #     result = Convert(result, dictionary)
    #     # template = loader.get_template('showresult.html')
    #     context = {
    #         'data2': result
    #     }
    #     context['data2'] = json.dumps(result)
    #     context['request'] = request
    #     print(type(context))
    #     print(result)
    #     return HttpResponse(template.render(context, request))
    # print('d2 ', context['data2'])
    return HttpResponse(template.render(context, request))

    # template_name = 'showresult.html'


class HomeView(TemplateView):
    template_name = 'index.html'
