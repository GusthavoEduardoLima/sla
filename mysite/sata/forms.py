from django import forms
from .models import Responsavel, CustomUser, Paciente, Profissional
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Paciente, Responsavel, CustomUser, Relacao

class RelacaoForm(forms.ModelForm):
    class Meta:
        model = Relacao
        fields = ['profissional'] 

class PacientesForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'cpf', 'nascimento', 'endereco', 'bairro', 'cep', 'cidade', 'estado', 'telefone', 'celular', 'sexo']

class ResponsaveisPacienteForm(forms.ModelForm):
    class Meta:
        model = Responsavel
        fields = ['nome', 'cpf', 'telefone', 'celular']

class UserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class ResponsaveisForm(forms.ModelForm):
    paciente = forms.ModelChoiceField(
        queryset=Paciente.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    class Meta:
        model = Responsavel
        fields = ['nome', 'cpf', 'telefone', 'celular']

class UserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class ProfissionalForm(forms.ModelForm):
    
    profissao_nome = forms.CharField(label="Profissão", widget=forms.TextInput(attrs={'class': 'form-control'}))
    instituicao_nome = forms.CharField(label="Instituição", widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Profissional
        fields = ['nome', 'cpf', 'telefone', 'celular'] 

    def save(self, commit=True):
        profissional = super(ProfissionalForm, self).save(commit=False)
        if commit:
            profissional.save()
        return profissional


# Definindo opções para as questões
OPCOES_QUESTAO = [
    (1, 'Opção 1'),
    (2, 'Opção 2'),
    (3, 'Opção 3'),
    (4, 'Opção 4'),
]

class CARSForm(forms.Form):
    choices1 = [
        (1, 'Nenhuma evidência de dificuldade ou anormalidade nas relações pessoais.'),
        (1.5, 'Intermediário'),
        (2, 'Relações levemente anormais.'),
        (2.5, 'Intermediário'),
        (3, 'Relações moderadamente anormais.'),
        (3.5, 'Intermediário'),
        (4, 'Relações gravemente anormais.')
    ]

    q1 = forms.ChoiceField(choices=choices1, widget=forms.RadioSelect(), label="Questão 1: Relações Pessoais")
    q2 = forms.ChoiceField(choices=choices1, widget=forms.RadioSelect(), label="Questão 2: Imitação")
    # Continue para as demais questões...
