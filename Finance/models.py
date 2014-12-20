from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
# Create your models here.

class Gruppo(models.Model):
    nome = models.CharField(verbose_name='Nome', max_length='200')
    icona = models.CharField(verbose_name='Icona', max_length='50', blank=True, null=True)
    ordine = models.IntegerField(verbose_name='Ordine',default=0)

    class Meta:
        verbose_name = 'Gruppo di costo'
        verbose_name_plural = 'Gruppi di costo'

    def __unicode__(self):
        return self.nome

    def get_centridicosto(self):
        return CentroDiCosto.objects.filter(gruppo=self)

    def get_valore(self):
        centridicosto=CentroDiCosto.objects.filter(gruppo=self)
        valore=Movimenti.objects.filter(centrodicosto__in=centridicosto).aggregate(Sum('valore'))['valore__sum']
        return valore

class CentroDiCosto (models.Model):
    nome = models.CharField(verbose_name='Nome', max_length='200')
    icona = models.CharField(verbose_name='Icona', max_length='50', blank=True, null=True)
    gruppo = models.ForeignKey(Gruppo,verbose_name='Gruppo',  blank=True, null=True)

    class Meta:
        verbose_name = 'Centro di costo'
        verbose_name_plural = 'Centri di costo'

    def __unicode__(self):
        return self.nome

    def get_valore(self):
        valore=Movimenti.objects.filter(centrodicosto=self).aggregate(Sum('valore'))['valore__sum']
        return valore


class Anagrafiche (models.Model):
    nome = models.CharField(verbose_name='Anagrafiche',max_length='200')

    class Meta:
        verbose_name = 'Anagrafica'
        verbose_name_plural = 'Anagrafiche'

    def __unicode__(self):
        return self.nome

    def get_valore(self):
        valore=Movimenti.objects.filter(fornitore=self).aggregate(Sum('valore'))['valore__sum']
        return valore

class CartaDiCredito(models.Model):
    nome = models.CharField(max_length='200', verbose_name='Nome')

    class Meta:
        verbose_name = 'Carta di Credito'
        verbose_name_plural = 'Carte di Credito'

    def __unicode__(self):
        return self.nome

class Movimenti (models.Model):
    persona = models.ForeignKey(User,blank=True,null=True)
    centrodicosto = models.ForeignKey(CentroDiCosto,blank=True,null=True)
    valore=models.DecimalField(verbose_name='Valore',max_digits=10,decimal_places=2)
    data = models.DateField(verbose_name='Data')
    descrizione = models.CharField(verbose_name='descrizione', max_length='200')
    fornitore = models.ForeignKey(Anagrafiche,verbose_name='fornitore',blank=True, null=True)
    cartadicredito=models.ForeignKey(CartaDiCredito,verbose_name='Carta di Credito', blank=True,null=True)

    anno=models.IntegerField(verbose_name='anno')
    mese=models.IntegerField(verbose_name='mese')
    class Meta:
        verbose_name = 'Movimento'
        verbose_name_plural = 'Movimenti'

    def __unicode__(self):
        return str(self.data) + ' ' + self.descrizione

