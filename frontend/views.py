import json

from django.db import models
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import FormularioForm
from example.models import Formulario
from django.utils import timezone 
from django.db.models import Count
from datetime import timedelta
# login screen

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # redirect based on role
            if hasattr(user, 'coordenador'):
                return redirect('home_coordenador')
            else:
                return redirect('cadastrar_formulario')
    else:
        form = AuthenticationForm()
    return render(request, 'frontend/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('')

def home_coordenador(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user

    # 1. SUPERUSUÁRIO: Vê absolutamente tudo (Acesso total)
    if user.is_superuser:
        formularios = Formulario.objects.all().order_by('-created_at')
    
    # 2. COORDENADOR: Vê APENAS os formulários dos usuários do seu setor
    elif hasattr(user, 'coordenador'):
        # Pegamos a lista de IDs dos setores que ele coordena
        meus_setores_ids = user.coordenador.setores.values_list('id', flat=True)
        
        # Filtramos formulários onde o setor do usuário está nessa lista
        formularios = Formulario.objects.filter(
            user__setor_id__in=meus_setores_ids
        ).distinct().order_by('-created_at')

    # 3. USUÁRIO COMUM OU STAFF SEM SETOR: Não deve ver dados de outros
    else:
        # Se você quiser que staff que não é coordenador não veja nada:
        if user.is_staff:
            formularios = Formulario.objects.none() 
        else:
            return redirect('cadastrar_formulario')

    return render(request, 'frontend/home_coordenador.html', {'formularios': formularios})


def dashboard_coordenador(request):
    if not hasattr(request.user, 'coordenador'):
        return redirect('home_admin')

    coord = request.user.coordenador
    meus_setores = coord.setores.all()
    
    # --- LÓGICA DE FILTRO POR TEMPO ---
    periodo = request.GET.get('periodo', '30') # Padrão 30 dias
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    # Filtro base por setor
    formularios_queryset = Formulario.objects.filter(
        user__setor__in=meus_setores
    ).distinct()

    # Aplica filtros de data
    if data_inicio and data_fim:
        formularios_queryset = formularios_queryset.filter(created_at__date__range=[data_inicio, data_fim])
    elif periodo == '0': # Hoje
        formularios_queryset = formularios_queryset.filter(created_at__date=timezone.now().date())
    elif periodo:
        dias = int(periodo)
        data_limite = timezone.now() - timedelta(days=dias)
        formularios_queryset = formularios_queryset.filter(created_at__gte=data_limite)

    # --- KPIs ---
    total_formularios = formularios_queryset.count()
    criticos = formularios_queryset.filter(estado__in=['alerta', 'risco']).count()
    hoje_count = formularios_queryset.filter(created_at__date=timezone.now().date()).count()

    # --- Gráfico de Estados ---
    estado_counts = formularios_queryset.values('estado').annotate(count=Count('id'))
    choices_dict = dict(Formulario.Estado.choices)
    estado_labels = [choices_dict.get(item['estado'], item['estado']) for item in estado_counts]
    estado_values = [item['count'] for item in estado_counts]

    # --- Gráfico de Influências ---
    influence_counter = {}
    for f in formularios_queryset:
        if isinstance(f.influencias, list):
            for inf in f.influencias:
                influence_counter[inf] = influence_counter.get(inf, 0) + 1

    influence_labels = list(influence_counter.keys())
    influence_values = list(influence_counter.values())

    context = {
        'coord': coord,
        'setores': meus_setores,
        'total_formularios': total_formularios,
        'criticos': criticos,
        'hoje': hoje_count,
        'estado_labels': json.dumps(estado_labels),
        'estado_values': json.dumps(estado_values),
        'influence_labels': json.dumps(influence_labels),
        'influence_values': json.dumps(influence_values),
        # Passar os filtros atuais de volta para o template
        'filtros': {
            'periodo': periodo,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
        }
    }
    return render(request, 'frontend/dashboard_coordenador.html', context)

def cadastrar_formulario(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = FormularioForm(request.POST)
        if form.is_valid():
            formulario = form.save(commit=False)
            formulario.user = request.user
            formulario.save()
            return redirect('cadastrar_formulario')
    else:
        form = FormularioForm()
    return render(request, 'frontend/cadastrar_formulario.html', {'form': form})