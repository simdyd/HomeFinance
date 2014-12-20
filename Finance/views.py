from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden,Http404
from django.core.exceptions import PermissionDenied
from django.template import RequestContext
from django.template import Context, loader
from Finance.models import CentroDiCosto,Gruppo,Movimenti,Anagrafiche,CartaDiCredito
from django.contrib.auth.models import User
from Finance.forms import addMovimento
from django.db.models import Sum
from datetime import timedelta,date
# Create your views here.
def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/userauth/login/?next=%s' % request.path)
    parameters ={}
    lista_gruppi=Gruppo.objects.all()
    data=date.today()
    uscite_gruppo_mc=Movimenti.objects.filter(valore__lt=0,anno=data.year,mese=data.month).values('centrodicosto__gruppo__nome').annotate(valore_sum=Sum('valore')).order_by('-valore_sum')
    data=data-timedelta(days=30)
    uscite_gruppo_mp=Movimenti.objects.filter(valore__lt=0,anno=data.year,mese=data.month).values('centrodicosto__gruppo__nome').annotate(valore_sum=Sum('valore')).order_by('-valore_sum')

    uscite=Movimenti.objects.filter(valore__lt=0).values('anno','mese').annotate(Sum('valore')).order_by('anno','mese')
    entrate=Movimenti.objects.filter(valore__gt=0).values('anno','mese').annotate(Sum('valore')).order_by('anno','mese')
    saldo=Movimenti.objects.all().aggregate(valore=Sum('valore'))['valore']

    parameters['lista_gruppi']=lista_gruppi
    parameters['uscite']=uscite
    parameters['entrate']=entrate
    parameters['saldo']=saldo
    print uscite_gruppo_mc
    parameters['uscite_gruppo_mc']=uscite_gruppo_mc
    parameters['uscite_gruppo_mp']=uscite_gruppo_mp
    
    t = loader.get_template('page/home.html')
    c = RequestContext( request, parameters)
    return HttpResponse(t.render(c))


def fornitori(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/userauth/login/?next=%s' % request.path)
    parameters ={}
    lista_fornitori=Anagrafiche.objects.all().order_by('nome')
    parameters['lista_fornitori']=lista_fornitori
    t = loader.get_template('page/lista_fornitori.html')
    c = RequestContext( request, parameters)
    return HttpResponse(t.render(c))

def ultimi_movimenti(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/userauth/login/?next=%s' % request.path)
    parameters ={}
    lista_movimenti=Movimenti.objects.all().order_by('-data')[:50]
    parameters['lista_movimenti']=lista_movimenti
    t = loader.get_template('page/ultimi_movimenti.html')
    c = RequestContext( request, parameters)
    return HttpResponse(t.render(c))

def elenco_gruppi(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/userauth/login/?next=%s' % request.path)
    parameters ={}
    lista_gruppi=Gruppo.objects.all()


    parameters['lista_gruppi']=lista_gruppi


    t = loader.get_template('page/elenco_gruppi.html')
    c = RequestContext( request, parameters)
    return HttpResponse(t.render(c))

def dettaglio_cdc(request,cdc_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/userauth/login/?next=%s' % request.path)
    parameters={}



    centrodicosto=CentroDiCosto.objects.get(id=cdc_id)
    entrate=Movimenti.objects.filter(centrodicosto=centrodicosto).values('anno','mese').annotate(Sum('valore')).order_by('anno','mese')
    movimenti_fornitore=Movimenti.objects.filter(centrodicosto=centrodicosto).values('fornitore__nome').annotate(valore_sum=Sum('valore')).order_by('-valore_sum')
    lista_movimenti=Movimenti.objects.filter(centrodicosto=centrodicosto).order_by('-data')

    parameters['entrate']=entrate
    parameters['movimenti_fornitore']=movimenti_fornitore
    parameters['centrodicosto']=centrodicosto
    parameters['lista_movimenti']=lista_movimenti
    t = loader.get_template('page/dettaglio_centro_di_costo.html')
    c = RequestContext( request, parameters)
    return HttpResponse(t.render(c))

def salva_movimento(forms,movimento):
    movimento.data=forms.cleaned_data['data']
    movimento.anno=movimento.data.year
    movimento.mese=movimento.data.month
    movimento.descrizione=forms.cleaned_data['descrizione']

    try:
        persona_id=forms.cleaned_data['persona']
        persona=User.objects.get(id=persona_id)
        movimento.persona=persona
    except:
        movimento.persona=None

    try:
        fornitore_id=forms.cleaned_data['fornitore']
        fornitore=Anagrafiche.objects.get(id=fornitore_id)
        movimento.fornitore=fornitore
    except:
        movimento.fornitore=None

    try:
        cartadicredito_id=forms.cleaned_data['carta']
        carta=CartaDiCredito.objects.get(id=cartadicredito_id)
        movimento.cartadicredito=carta
    except:
        movimento.cartadicredito=None
    movimento.valore=forms.cleaned_data['valore']

    centrodicosto_id=forms.cleaned_data['centrodicosto']

    movimento.centrodicosto=CentroDiCosto.objects.get(id=centrodicosto_id)


    movimento.save()


def modifica_movimento(request,movimento_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/userauth/login/?next=%s' % request.path)
    parameters={}
    movimento=Movimenti.objects.get(id=movimento_id)
    if request.method=='POST':
        forms=addMovimento(request.POST)
        if forms.is_valid():
            salva_movimento(forms,movimento)

            return HttpResponseRedirect('/dettaglio_cdc/' + str(movimento.centrodicosto.id) +'/')
    else:
        #forms=addMovimento()
        if movimento.fornitore:
            fornitore_id=movimento.fornitore.id
        else:
            fornitore_id=None

        if movimento.persona:
            persona_id=movimento.persona.id
        else:
            persona_id=None

        if movimento.cartadicredito:
            carta_id=movimento.cartadicredito.id
        else:
            carta_id=None
        data=movimento.data.strftime('%Y-%m-%d')

        forms = addMovimento(initial={'centrodicosto': movimento.centrodicosto.id,
                                      'persona':persona_id,
                                      'carta': carta_id,
                                      'descrizione':movimento.descrizione,
                                      'data':data,
                                      'fornitore':fornitore_id,
                                      'valore':movimento.valore})

    #if cdc_id is not None:
    #    parameters['cdc_id']=cdc_id

    parameters['forms']=forms
    t = loader.get_template('page/new_movimento.html')
    c = RequestContext( request, parameters)
    return HttpResponse(t.render(c))

def new_movimento(request,cdc_id=None):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/userauth/login/?next=%s' % request.path)
    parameters={}

    if request.method=='POST':
        forms=addMovimento(request.POST)
        if forms.is_valid():
            movimento=Movimenti()

            salva_movimento(forms,movimento)

            return HttpResponseRedirect('/dettaglio_cdc/'+ str(movimento.centrodicosto.id) +'/')
    else:
        #forms=addMovimento()
        forms = addMovimento(initial={'centrodicosto': cdc_id,'persona':request.user.id})

    #if cdc_id is not None:
    #    parameters['cdc_id']=cdc_id

    parameters['forms']=forms
    t = loader.get_template('page/new_movimento.html')
    c = RequestContext( request, parameters)
    return HttpResponse(t.render(c))