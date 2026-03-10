from django.urls import path
from .views import login_view, logout_view, home_coordenador, dashboard_coordenador, cadastrar_formulario

urlpatterns = [
    path('login/', login_view, name='login'),
    path('', login_view),
    path('logout/', logout_view, name='logout'),
    path('home_coordenador/', home_coordenador, name='home_coordenador'),
    path('dashboard_coordenador/', dashboard_coordenador, name='dashboard_coordenador'),
    path('cadastrar_formulario/', cadastrar_formulario, name='cadastrar_formulario'),
]