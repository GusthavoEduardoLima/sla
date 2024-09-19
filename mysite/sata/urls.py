from django.urls import path
from .views import avaliacao,avaliacao_cars, relatorio_cars_view,grafico_cars_view,pacientes, responsaveis, profissionais, inicio, registrar_responsavel, registrar_paciente, registrar_profissional, profissionais_relacionados,remover_relacao,ProfissionalDetailView, ProfissionalUpdateView, ProfissionalDeleteView, ResponsavelDatailView, ResponsavelDeleteView, ResponsavelUpdateView, PacienteDeleteView, PacienteUpadateView, PacienteDatailView
from django.contrib.auth import views as auth_views

from django.urls import include


urlpatterns = [
    path('pacientes/', pacientes, name='pacientes'),
    path('responsaveis/', responsaveis, name='responsaveis'),
    path('profissionais/', profissionais, name='profissionais'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', inicio, name='inicio'),
    path('registrar-responsavel/', registrar_responsavel, name='registrar_responsavel'),
    path('registrar-paciente/', registrar_paciente, name='registrar_paciente' ),
    path('registrar-profissional/', registrar_profissional, name='registrar_profissional' ),

    path('profissional/<int:pk>/', ProfissionalDetailView.as_view(), name='visualizar_profissional'),
    path('profissional/<int:pk>/editar/', ProfissionalUpdateView.as_view(), name='editar_profissional'),
    path('profissional/<int:pk>/deletar/', ProfissionalDeleteView.as_view(), name='deletar_profissional'),

    path('responsavel/<int:pk>/', ResponsavelDatailView.as_view(), name='visualizar_responsavel'),
    path('responsavel/<int:pk>/editar/', ResponsavelUpdateView.as_view(), name='editar_responsavel'),
    path('responsavel/<int:pk>/deletar/', ResponsavelDeleteView.as_view(), name='deletar_responsavel'),

    path('paciente/<int:pk>/', PacienteDatailView.as_view(), name='visualizar_pacientes'),
    path('paciente/<int:pk>/editar/', PacienteUpadateView.as_view(), name='editar_paciente'),
    path('paciente/<int:pk>/deletar/', PacienteDeleteView.as_view(), name='deletar_paciente'),

    path('avaliacao/<int:paciente_id>/', avaliacao_cars, name='avaliacao_cars'),
    path('avaliacao/', avaliacao, name='avaliacao'),
    path('relatorio', grafico_cars_view, name='relatorio'),
    path('grafico-pacientes', relatorio_cars_view, name='grafico'),

    path('paciente/<int:paciente_id>/profissionais/', profissionais_relacionados, name='profissionais_relacionados'),
    path('paciente/<int:paciente_id>/profissional/<int:profissional_id>/remover/', remover_relacao, name='remover_relacao'),


]
