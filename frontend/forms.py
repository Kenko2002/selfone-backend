from django import forms
from example.models import Formulario


class FormularioForm(forms.ModelForm):
    ESTADO_CHOICES = [
        (Formulario.Estado.ESTAVEL, "Estável"),
        (Formulario.Estado.ATENCAO, "Em Atenção"),
        (Formulario.Estado.ALERTA, "Em Alerta"),
        (Formulario.Estado.RISCO, "Em Risco"),
    ]

    INFLUENCIAS_CHOICES = [
        ("Contexto pessoal", "Contexto pessoal"),
        ("Sobrecarga de Tarefas", "Sobrecarga de Tarefas"),
        ("Falta de Clareza", "Falta de Clareza"),
        ("Conflito", "Conflito"),
        ("Processo desorganizado", "Processo desorganizado"),
        ("Comunicação inadequada", "Comunicação inadequada"),
    ]

    estado = forms.ChoiceField(choices=ESTADO_CHOICES, initial=Formulario.Estado.ESTAVEL)
    influencias = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=INFLUENCIAS_CHOICES,
    )
    texto_livre = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "cols": 40,
                "class": "form-control bg-dark text-light",
                "style": "border: 1px solid rgba(255,255,255,0.85); border-radius: 0.375rem;",
            }
        ),
        label="Campo de Texto Livre",
    )

    class Meta:
        model = Formulario
        fields = ['estado', 'influencias', 'descricao', 'texto_livre']
        widgets = {
            'descricao': forms.Textarea(
                attrs={
                    'rows': 4,
                    'cols': 40,
                    'class': 'form-control bg-dark text-light',
                    'style': 'border: 1px solid rgba(255,255,255,0.85); border-radius: 0.375rem;',
                }
            ),
            'texto_livre': forms.Textarea(
                attrs={
                    'rows': 4,
                    'cols': 40,
                    'class': 'form-control bg-dark text-light',
                    'style': 'border: 1px solid rgba(255,255,255,0.85); border-radius: 0.375rem;',
                }
            ),
        }

    def clean_influencias(self):
        return self.cleaned_data.get('influencias', [])

    def clean_texto_livre(self):
        from django.utils.html import strip_tags

        texto = self.cleaned_data.get('texto_livre', '') or ''
        # Remove qualquer HTML para manter o campo como texto limpo.
        return strip_tags(texto).strip()
