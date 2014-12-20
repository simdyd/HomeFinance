from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.template import RequestContext
from django.template import Context, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
def agenti_login(request):
    message=''
    if request.method == 'POST': # If the form has been submitted...
        username = request.POST['username']
        password = request.POST['password']




        user = authenticate(username=username, password=password)
        try:
            next=request.POST['next']
        except:
            next='/'



        if user is not None:
            if user.is_active:

                login(request, user)
                result='ok'
                message=''
                return HttpResponseRedirect(next)
            else:
                result='ko'
                message='Il tuo account &egrave; stato disabilitato'

        else:
            result='ko'
            message = 'username o password errate'

            #print "Your username and password were incorrect."
    else:
        try:
            next=request.GET['next']
        except:
            next='/'

    page_title=settings.SITE_TITLE
    page_subtitle='Login'
    parameters={}
    parameters['message'] = message
    parameters['next'] = next
    parameters['site_title'] = page_title
    parameters['page_subtitle'] = page_subtitle

    #parameters['email_assistenza'] = settings.EMAIL_ASSISTENZA

    #parameters['current_page'] = '/userauth/login/'
    #parameters['block'] = 'block/block_login.html'

    t = loader.get_template('page/login.html')
    c = RequestContext( request, parameters)
    return HttpResponse(t.render(c))


def logout_view(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/userauth/login/?next=%s' % request.path)

    logout(request)
    page_subtitle='Logout'
    parameters={}
    parameters['site_title'] = settings.SITE_TITLE
    parameters['page_subtitle'] = page_subtitle

    #parameters['email_assistenza'] = settings.EMAIL_ASSISTENZA


    t = loader.get_template( 'page/login.html')
    c = RequestContext( request, parameters)
    return HttpResponse(t.render(c))