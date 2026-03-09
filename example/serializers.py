from rest_framework import serializers
from .models import (
    User,
    Formulario,
    UnidadeOrganizacional,
    Setor,
    Coordenador,
)


class UnidadeOrganizacionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadeOrganizacional
        fields = ['id', 'nome', 'qtd_max_usuarios', 'qtd_max_coordenadores']


class SetorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setor
        fields = ['id', 'nome', 'unidade']


class CoordenadorSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True,
    )
    setores = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Setor.objects.all(),
        required=False,
    )

    class Meta:
        model = Coordenador
        fields = ['id', 'user', 'nome', 'matricula', 'setores']


class UserSerializer(serializers.ModelSerializer):
    nome = serializers.ReadOnlyField()
    setor = serializers.PrimaryKeyRelatedField(
        queryset=Setor.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'nome',
            'bio',
            'setor',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        setor = validated_data.pop('setor', None)
        user = User.objects.create_user(**validated_data)
        if setor is not None:
            user.setor = setor
            user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class FormularioSerializer(serializers.ModelSerializer):
    data_cadastro = serializers.ReadOnlyField(source='created_at')
    estado = serializers.ChoiceField(choices=Formulario.Estado.choices)
    influencias = serializers.ListField(
        child=serializers.CharField(), required=False, allow_empty=True
    )
    texto_livre = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Formulario
        fields = ['id', 'user', 'data_cadastro', 'estado', 'influencias', 'descricao', 'texto_livre']
        read_only_fields = ['id', 'data_cadastro']
