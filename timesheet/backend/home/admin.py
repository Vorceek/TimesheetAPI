from django.contrib import admin
from .models import  Setor, Colaborador
from django.utils.html import format_html

class SetorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ver_colaboradores')

    def ver_colaboradores(self, obj):
        colaboradores = obj.get_colaboradores()
        # Gera links para os colaboradores
        links = [format_html('<a href="/admin/auth/user/{}/change/">{}</a>', colaborador.id, colaborador.nome.username) for colaborador in colaboradores]
        return format_html(", ".join(links)) if colaboradores else "Nenhum colaborador"
    
    ver_colaboradores.short_description = 'Colaboradores'

admin.site.register(Setor, SetorAdmin)

class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'get_setores')
    list_display_links = ('id', 'nome')

    def get_setores(self, obj):
        # Exibe os setores aos quais o colaborador pertence
        return ", ".join([setor.nome for setor in obj.setores.all()]) if obj.setores.exists() else "Nenhum setor"

    get_setores.short_description = 'Setores'

    # Para permitir a edição dos setores no admin
    filter_horizontal = ('setores',)

admin.site.register(Colaborador, ColaboradorAdmin)
