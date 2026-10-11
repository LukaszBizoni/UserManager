from django import forms

from .models import Usuario


class UsuarioForm(forms.ModelForm):
    nome = forms.CharField(
        label="Nome",
        min_length=2,
        max_length=255,
        error_messages={
            "required": "Informe o nome do usuário.",
            "min_length": "O nome deve ter pelo menos 2 caracteres.",
            "max_length": "O nome deve ter no máximo 255 caracteres.",
        },
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Digite o nome",
                "autocomplete": "name",
            }
        ),
    )
    idade = forms.IntegerField(
        label="Idade",
        min_value=0,
        max_value=130,
        error_messages={
            "required": "Informe a idade do usuário.",
            "invalid": "Informe uma idade válida.",
            "min_value": "A idade não pode ser negativa.",
            "max_value": "Informe uma idade de até 130 anos.",
        },
        widget=forms.NumberInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Digite a idade",
                "inputmode": "numeric",
            }
        ),
    )

    class Meta:
        model = Usuario
        fields = ("nome", "idade")

    def clean_nome(self):
        nome = self.cleaned_data["nome"].strip()
        if not nome:
            raise forms.ValidationError("Informe o nome do usuário.")
        return nome
