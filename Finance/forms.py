from django import forms
from Finance.models import CentroDiCosto,Anagrafiche,CartaDiCredito
from django.contrib.auth.models import User

    #persona = models.ForeignKey(User,blank=True,null=True)
    #centrodicosto = models.ForeignKey(CentroDiCosto,blank=True,null=True)
    #valore=models.DecimalField(verbose_name='Valore',max_digits=10,decimal_places=2)
    #data = models.DateField(verbose_name='Data')
    #descrizione = models.CharField(verbose_name='descrizione', max_length='200')
    #fornitore = models.ForeignKey(Anagrafiche,verbose_name='fornitore',blank=True, null=True)

class addMovimento(forms.Form):
    cdc_choices = [(cdc.id, cdc.gruppo.nome + ' - ' + cdc.nome) for cdc in CentroDiCosto.objects.all().order_by('gruppo__ordine')]
    persona_choices =[('','Nessuno')]
    persona_choices += [(persona.id, persona.username) for persona in User.objects.all().order_by('username')]

    anagrafiche_choices =[('','Nessuno')]
    anagrafiche_choices += [(anagrafica.id, anagrafica.nome) for anagrafica in Anagrafiche.objects.all().order_by('nome')]

    carte_choices =[('','Nessuno')]
    carte_choices+=[(carta.id, carta.nome) for carta in CartaDiCredito.objects.all().order_by('nome')]

    #carte_choices.append(('','Nessuno'))
    data=forms.DateField(label=u'data',widget=forms.widgets.DateInput(attrs={'class':'form-control','type':'date'},format="%d-%m-%Y"))
    descrizione=forms.CharField(label=u'descrizione',widget=forms.widgets.Textarea(attrs={'class':'form-control'}),required=True)
    persona=forms.IntegerField(label=u'Persona',required=False,widget=forms.Select(attrs={'class':'form-control'},choices=persona_choices))
    fornitore=forms.IntegerField(label=u'Fornitore',required=False,widget=forms.Select(attrs={'class':'form-control chzn-nopadd chzn-select-deselect'},choices=anagrafiche_choices))
    carta=forms.IntegerField(label=u'Carta di Credito',required=False,widget=forms.Select(attrs={'class':'form-control'},choices=carte_choices))
    valore=forms.DecimalField(label=u'Valore',widget=forms.widgets.Input(attrs={'class':'form-control','type':'number'}))
    centrodicosto=forms.IntegerField(widget=forms.Select(attrs={'class':'form-control'},choices=cdc_choices))
