from django.contrib import admin
from core.models import Empresas, Listas, AuxListas

# Register your models here.
class EmpresasAdmin(admin.ModelAdmin):
    pass

class ListasAdmin(admin.ModelAdmin):
    pass

class AuxListasAdmin(admin.ModelAdmin):
    pass

admin.site.register(Empresas, EmpresasAdmin)
admin.site.register(Listas, ListasAdmin)
admin.site.register(AuxListas, AuxListasAdmin)