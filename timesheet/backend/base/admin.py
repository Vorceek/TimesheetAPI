from django.contrib import admin
from .models import Cliente, RegistroAtividade, Servico, Atividade
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.utils.timezone import localtime

# CLIENTE
class ClienteResource(resources.ModelResource):
    class Meta:
        model = Cliente
        fields = ('nome', 'setor')
        list_display_links = ('id', 'nome', 'setor')

    def before_import_row(self, row, **kwargs):
        row['id'] = None

@admin.register(Cliente)
class ClienteAdmin(ImportExportModelAdmin):
    resource_class = ClienteResource
    list_display = ('id', 'nome', 'get_setores')
    list_display_links = ('id', 'nome', 'get_setores')
    filter_horizontal = ('setor', 'servicos')  # Remover 'get_setores', pois é um método

    def get_setores(self, obj):
        return ", ".join([grupo.name for grupo in obj.setor.all()])
    get_setores.short_description = 'Setores'


# SERVIÇO
class ServicoResource(resources.ModelResource):
    class Meta:
        model = Servico
        fields = ('nome', 'setor')

@admin.register(Servico)
class ServicoAdmin(ImportExportModelAdmin):
    resource_class = ServicoResource
    list_display = ('id', 'nome', 'get_setores')
    list_display_links = ('id', 'nome', 'get_setores')
    filter_horizontal = ('setor', 'atividades')

    def get_setores(self, obj):
        return ", ".join([grupo.name for grupo in obj.setor.all()])
    get_setores.short_description = 'Setores'


# ATIVIDADE
class AtividadeResource(resources.ModelResource):
    class Meta:
        model = Atividade
        fields = ('nome', 'setor')

@admin.register(Atividade)
class AtividadeAdmin(ImportExportModelAdmin):
    resource_class = AtividadeResource
    list_display = ('id', 'nome', 'get_setores')
    list_display_links = ('id', 'nome', 'get_setores')
    filter_horizontal = ('setor',)  # Remover 'get_setores', pois é um método

    def get_setores(self, obj):
        return ", ".join([grupo.name for grupo in obj.setor.all()])
    get_setores.short_description = 'Setores'


# REGISTRO ATIVIDADE
class RegistroAtividadeAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'servico', 'atividade', 'hora_formatada', 'data_final', 'duracao')
    list_display_links = ('id', 'cliente', 'servico')
    fields = ['cliente', 'servico', 'atividade']
    list_filter = ('cliente', 'servico', 'atividade', 'data_inicial')

    def hora_formatada(self, obj):
        return localtime(obj.data_inicial).strftime('%d/%m/%Y %H:%M')  # Corrigido para 'data_inicial'
    
    hora_formatada.short_description = 'Hora'

admin.site.register(RegistroAtividade, RegistroAtividadeAdmin)
