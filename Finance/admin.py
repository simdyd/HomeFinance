from django.contrib import admin
from Finance.models import *

# Register your models here.

class CentroDiCostoAdmin(admin.ModelAdmin):
    list_display = ('nome','gruppo')
    list_filter =[ 'gruppo',]
    save_as = True
    save_on_top = True

admin.site.register(CentroDiCosto,CentroDiCostoAdmin)

class CartaDiCreditoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    #list_filter =[ 'gruppo',]
    save_as = True
    save_on_top = True
admin.site.register(CartaDiCredito,CartaDiCreditoAdmin)

admin.site.register(Anagrafiche)

admin.site.register(Movimenti)

admin.site.register(Gruppo)