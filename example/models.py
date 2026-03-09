from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Adiciona campos personalizados se necessário
    # Por exemplo, um campo adicional
    bio = models.TextField(blank=True, null=True)

    setor = models.ForeignKey(
        "Setor",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="usuarios",
    )

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    @property
    def nome(self):
        full = self.get_full_name()
        return full or self.username


class Formulario(models.Model):
    class Estado(models.TextChoices):
        ESTAVEL = "estavel", "Estável"
        ATENCAO = "atencao", "Em Atenção"
        ALERTA = "alerta", "Em Alerta"
        RISCO = "risco", "Em Risco"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='formularios')
    created_at = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.ESTAVEL)
    influencias = models.JSONField(default=list, blank=True)
    descricao = models.TextField()
    texto_livre = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Formulário'
        verbose_name_plural = 'Formulários'

    def __str__(self):
        return f"Formulário de {self.user.username} em {self.created_at}"

    def influencias_display(self):
        if isinstance(self.influencias, (list, tuple)):
            return ", ".join(self.influencias)
        return str(self.influencias)

    influencias_display.short_description = "Influências"


class UnidadeOrganizacional(models.Model):
    nome = models.CharField(max_length=255)
    qtd_max_usuarios = models.PositiveIntegerField(default=0)
    qtd_max_coordenadores = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Unidade Organizacional"
        verbose_name_plural = "Unidades Organizacionais"

    def __str__(self):
        return self.nome


class Setor(models.Model):
    nome = models.CharField(max_length=255)
    unidade = models.ForeignKey(
        UnidadeOrganizacional,
        on_delete=models.CASCADE,
        related_name="setores",
    )

    class Meta:
        verbose_name = "Setor"
        verbose_name_plural = "Setores"

    def __str__(self):
        return self.nome


class Coordenador(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="coordenador",
        null=True,
        blank=True,
    )
    nome = models.CharField(max_length=255)
    matricula = models.CharField(max_length=100)
    setores = models.ManyToManyField(Setor, related_name="coordenadores", blank=True)

    class Meta:
        verbose_name = "Coordenador"
        verbose_name_plural = "Coordenadores"

    def __str__(self):
        display = self.nome
        if self.user and self.user.username:
            display = f"{self.nome} ({self.user.username})"
        return f"{display} ({self.matricula})"