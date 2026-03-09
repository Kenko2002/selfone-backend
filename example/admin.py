from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import (
    User,
    Formulario,
    UnidadeOrganizacional,
    Setor,
    Coordenador,
)

# 1. Inline de Usuários para ser usado dentro do Setor
class UserInline(admin.TabularInline):
    model = User
    fields = ('username', 'email', 'is_active')
    extra = 0  # Não exibe linhas vazias extras por padrão
    show_change_link = True # Permite clicar para ir editar o usuário completo

@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'unidade')
    list_filter = ('unidade',)
    inlines = [UserInline] # Adiciona os usuários aqui

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    # Adicionando o campo 'setor' e 'bio' na interface de edição do usuário
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('setor', 'bio')}),
    )
    # Adicionando setor na lista de usuários
    list_display = DjangoUserAdmin.list_display + ('setor',)
    list_filter = DjangoUserAdmin.list_filter + ('setor',)

@admin.register(UnidadeOrganizacional)
class UnidadeOrganizacionalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'qtd_max_usuarios', 'qtd_max_coordenadores')

@admin.register(Coordenador)
class CoordenadorAdmin(admin.ModelAdmin):
    list_display = ('user', 'nome', 'matricula')
    raw_id_fields = ('user',)
    filter_horizontal = ('setores',) # Melhora a seleção de múltiplos setores

@admin.register(Formulario)
class FormularioAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'estado', 'influencias_display')
    readonly_fields = ('created_at',)
    search_fields = ('user__username', 'descricao', 'texto_livre')
    list_filter = ('estado',)