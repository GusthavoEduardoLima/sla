from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Paciente, Profissional, Responsavel, Relacao
from .decorators import nivel_acesso_requerido
from django.shortcuts import render, redirect
from .forms import ResponsaveisForm, ResponsaveisPacienteForm,UserForm, PacientesForm, ProfissionalForm, RelacaoForm
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Profissional, Instituicao, Profissao
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView



class ProfissionalDeleteView(DeleteView):
    model = Profissional
    template_name = 'modulo_gerencial/profissional_confirm_delete.html'
    success_url = reverse_lazy('profissionais')
class ResponsavelDeleteView(DeleteView):
    model = Responsavel
    template_name = 'modulo_gerencial/responsavel_confirm_delete.html'
    success_url = reverse_lazy('responsaveis')

class PacienteDeleteView(DeleteView):
    model = Paciente
    template_name = 'modulo_gerencial/paciente_confirm_delete.html'
    success_url = reverse_lazy('pacientes')

class ProfissionalUpdateView(UpdateView):
    model = Profissional
    fields = ['nome',  'telefone', 'cpf', 'celular',   'profissao', 'instituicao']
    template_name = 'modulo_gerencial/profissional_form.html'
    success_url = reverse_lazy('profissionais')

class ResponsavelUpdateView(UpdateView):
    model = Responsavel
    fields = ['nome', 'telefone', 'cpf']
    template_name = 'modulo_gerencial/responsavel_form.html'
    success_url = reverse_lazy('responsaveis')

class PacienteUpadateView(UpdateView):
    model = Paciente
    fields = ['nome', 'cpf', 'nascimento', 'endereco', 'bairro', 'cep', 'cidade', 'estado', 'telefone', 'celular', 'sexo']
    template_name = 'modulo_gerencial/paciente_form.html'
    success_url = reverse_lazy('pacientes')

class ProfissionalDetailView(DetailView):
    model = Profissional
    template_name = 'modulo_gerencial/profissional_detalhe.html'

class ResponsavelDatailView(DetailView):
    model = Responsavel
    template_name  = 'modulo_gerencial/responsavel_detalhe.html'

class PacienteDatailView(DetailView):
    model = Paciente
    template_name = 'modulo_gerencial/paciente_detalhe.html'



def remover_relacao():
    pass


@login_required
@nivel_acesso_requerido(3)
def profissionais_relacionados(request, paciente_id):
    paciente = get_object_or_404(Paciente, pk=paciente_id)
    profissionais = Profissional.objects.filter(relacao__paciente=paciente)  # Profissionais já relacionados
    
    if request.method == 'POST':
        relacao_form = RelacaoForm(request.POST)
        if relacao_form.is_valid():
            relacao = relacao_form.save(commit=False)
            relacao.paciente = paciente
            relacao.save()
            return redirect('profissionais_relacionados', paciente_id=paciente_id)  # Atualiza a página
    else:
        relacao_form = RelacaoForm()

    return render(request, 'modulo_gerencial/profissionais_relacionados.html', {
        'paciente': paciente,
        'profissionais': profissionais,
        'relacao_form': relacao_form
    })
@login_required
@nivel_acesso_requerido(2)  # Usuários com nível 2 e acima podem acessar
def pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'modulo_gerencial/pacientes.html', {'pacientes': pacientes})
@login_required
@nivel_acesso_requerido(2)
def registrar_paciente(request):
    if request.method == 'POST':
        paciente_form = PacientesForm(request.POST)
        responsavel_form = ResponsaveisPacienteForm(request.POST)
        user_form = UserForm(request.POST)
        
        if paciente_form.is_valid() and responsavel_form.is_valid() and user_form.is_valid():
            # Cria o usuário (CustomUser)
            user = user_form.save(commit=False)
            user.nivel_acesso = 2  # Define o nível de acesso para o responsável
            user.save()
            
            # Cria o responsável e relaciona com o CustomUser criado
            responsavel = responsavel_form.save(commit=False)
            responsavel.user = user
            responsavel.save()

            # Cria o paciente e relaciona com o responsável
            paciente = paciente_form.save(commit=False)
            paciente.responsavel = responsavel
            paciente.user = request.user  # Relaciona o paciente ao usuário atual (profissional)
            paciente.save()

            return redirect('pacientes')  # Redireciona após o sucesso
    else:
        paciente_form = PacientesForm()
        responsavel_form = ResponsaveisPacienteForm()
        user_form = UserForm()

    return render(request, 'modulo_gerencial/registrar_paciente.html', {
        'paciente_form': paciente_form,
        'responsavel_form': responsavel_form,
        'user_form': user_form,
    })


@login_required
@nivel_acesso_requerido(2)  # Usuários com nível 2 e acima podem acessar
def responsaveis(request):
    responsaveis = Responsavel.objects.all()

    return render(request, 'modulo_gerencial/responsaveis.html',{'responsaveis': responsaveis})

@login_required
@nivel_acesso_requerido(2)
def registrar_responsavel(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        responsavel_form = ResponsaveisForm(request.POST)
        
        if user_form.is_valid() and responsavel_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])  # Define a senha
            user.nivel_acesso = 2
            user.save()  # Salva o usuário no banco de dados

            responsavel = responsavel_form.save(commit=False)
            responsavel.user = user  # Relaciona o responsável com o usuário criado
            responsavel.save()  # Salva o responsável no banco de dados
            
            
            return render(request, 'modulo_gerencial/responsaveis.html')  # Redireciona para a lista de responsáveis
       
       
    else:
        user_form = UserForm()
        responsavel_form = ResponsaveisForm()

    return render(request, 'modulo_gerencial/registrar_responsavel.html', {
        'user_form': user_form,
        'responsavel_form': responsavel_form
    })
@login_required
@nivel_acesso_requerido(3)  # Somente usuários com nível 3 podem acessar
def profissionais(request):
    profissionais = Profissional.objects.all()
    return render(request, 'modulo_gerencial/profissionais.html', {'profissionais': profissionais})

@login_required
@nivel_acesso_requerido(3)
def registrar_profissional(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profissional_form = ProfissionalForm(request.POST)
        if profissional_form.is_valid() and user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])  # Define a senha
            user.save()  # Salva o usuário no banco de dados


            # Verifica ou cria a profissão com base no nome informado
            profissao_nome = profissional_form.cleaned_data['profissao_nome']
            profissao, created = Profissao.objects.get_or_create(descricao=profissao_nome)

            # Verifica ou cria a instituição com base no nome informado
            instituicao_nome = profissional_form.cleaned_data['instituicao_nome']
            instituicao, created = Instituicao.objects.get_or_create(descricao=instituicao_nome)

            # Criação do profissional e vinculação com o usuário, profissão e instituição
            profissional = profissional_form.save(commit=False)
            profissional.user = user  # Relaciona o profissional com o usuário criado
            profissional.profissao = profissao  # Relaciona o profissional com a profissão criada/encontrada
            profissional.instituicao = instituicao  # Relaciona o profissional com a instituição criada/encontrada
            profissional.save()


            profissional = profissional_form.save(commit=False)
            profissional.user = user  # Relaciona o responsável com o usuário criado
            profissional.save()
            return render(request, 'modulo_gerencial/profissionais.html')
            
      
    else:
        profissional_form = ProfissionalForm()
        user_form = UserForm()
    return render(request, 'modulo_gerencial/registrar_profissional.html', {'profissional_form': profissional_form, 'user_form':user_form})


def inicio(request):
    return render(request, 'index.html')

# views.py
from django.shortcuts import render, redirect
from .forms import CARSForm
from .models import CARS, Relacao, Profissional, Paciente
from django.shortcuts import get_object_or_404, redirect, render
from .models import Paciente, Profissional, Relacao, CARS
from .forms import CARSForm
def avaliacao(request):
    pacientes = Paciente.objects.all()
    return render(request, 'modulo_funcional/pacientes_avaliacao.html', {'pacientes': pacientes})
@login_required
@login_required
def avaliacao_cars(request, paciente_id):
    profissional = get_object_or_404(Profissional, user=request.user)
    paciente = get_object_or_404(Paciente, pk=paciente_id)

    relacao, created = Relacao.objects.get_or_create(paciente=paciente, profissional=profissional)

    if 'questao_atual' not in request.session:
        request.session['questao_atual'] = 1

    total_questoes = 2

    form = CARSForm(request.POST or None)

    if request.method == 'POST':
        if 'avancar' in request.POST and form.is_valid():
            # Salva a resposta da questão atual na sessão
            questao_atual = request.session['questao_atual']
            request.session[f'q{questao_atual}'] = form.cleaned_data[f'q{questao_atual}']

            # Avança para a próxima questão
            if questao_atual < total_questoes:
                request.session['questao_atual'] += 1
            return redirect('avaliacao_cars', paciente_id=paciente_id)

        elif 'voltar' in request.POST:
            if request.session['questao_atual'] > 1:
                request.session['questao_atual'] -= 1
            return redirect('avaliacao_cars', paciente_id=paciente_id)

        elif 'finalizar' in request.POST and form.is_valid():
            # Captura todas as respostas da sessão
            respostas = {f'q{i}': request.session.get(f'q{i}') for i in range(1, total_questoes + 1)}
            resultado = sum(float(respostas.get(f'q{i}', 0) or 0) for i in range(1, total_questoes + 1))
            # Cria o registro CARS no banco de dados
            relacao = Relacao.objects.get(paciente=paciente, profissional=profissional)
            CARS.objects.create(
        relacao=relacao,
        q1=float(respostas.get('q1', 0) or 0),
        q2=float(respostas.get('q2', 0) or 0),
        # Continue adicionando as respostas para todas as questões...
        resultado=resultado
    )

            # Limpa a sessão após finalizar a avaliação
            for i in range(1, total_questoes + 1):
                request.session.pop(f'q{i}', None)
            request.session.pop('questao_atual', None)

            return redirect('avaliacao')

    # Preenche o formulário com as respostas salvas na sessão
    questao_atual = request.session['questao_atual']
    if f'q{questao_atual}' in request.session:
        form.initial[f'q{questao_atual}'] = request.session[f'q{questao_atual}']
    
    return render(request, 'modulo_funcional/avaliacao_cars.html', {
        'form': form,
        'questao_atual': questao_atual,
        'total_questoes': total_questoes,
        'paciente': paciente,
        'profissional': profissional
    })

import json
from django.db.models import Avg as avg

def grafico_cars_view(request):
  # Obter as avaliações do CARS
  avaliacoes = CARS.objects.all()

  # Formatar os dados para o Chart.js (médias por questão)
  labels = []  # Lista de datas das avaliações
  q1_data = []
  q2_data = []
  # ... (repetir para todas as questões)
  resultado_data = []

  for avaliacao in avaliacoes:
    # Extrair a data da avaliação
    labels.append(avaliacao.data_avaliacao.strftime('%Y-%m-%d'))

    # Calcular a média de cada questão (considerando todas as avaliações)
    q1_media = CARS.objects.filter(q1=avaliacao.q1).aggregate(avg('q1'))['q1__avg']
    q2_media = CARS.objects.filter(q2=avaliacao.q2).aggregate(avg('q2'))['q2__avg']
    # ... (repetir para todas as questões)
    resultado_media = CARS.objects.aggregate(avg('resultado'))['resultado__avg']

    # Adicionar as médias às listas de dados
    q1_data.append(q1_media)
    q2_data.append(q2_media)
    # ... (repetir para todas as questões)
    resultado_data.append(resultado_media)

  # Passar os dados para o template
  context = {
      'labels': json.dumps(labels),
      'q1_data': json.dumps(q1_data),
      'q2_data': json.dumps(q2_data),
      # ... (repetir para todas as questões)
      'resultado_data': json.dumps(resultado_data),
  }
  return render(request, 'modulo_funcional/grafico_cars.html', context)


def relatorio_cars_view(request):
    # Consulta para obter a média das avaliações por profissional
    dados_grafico = (
        CARS.objects.values('relacao__profissional__nome')
        .annotate(
            media_q1=avg('q1'),
            media_q2=avg('q2'),
            media_resultado=avg('resultado')
        )
    )

    # Convertendo o queryset em uma lista de dicionários
    dados_grafico_list = list(dados_grafico)

    # Serializar a lista de dados em formato JSON para passar ao template
    dados_grafico_json = json.dumps(dados_grafico_list)

    # Renderizando a view e passando os dados para o template
    return render(request, 'modulo_funcional/grafico_pacientes.html', {
        'dados_grafico': dados_grafico_json
    })