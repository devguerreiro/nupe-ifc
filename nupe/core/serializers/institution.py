from rest_framework.serializers import ModelSerializer, ValidationError
from validate_docbr.CNPJ import CNPJ

from nupe.core.models import Campus, Institution
from nupe.core.serializers.location import LocationSerializer
from nupe.resources.messages.institution import CAMPUS_INVALID_CNPJ_MESSAGE


class InstitutionSerializer(ModelSerializer):
    """
    Recebe e valida informações para então cadastrar ou atualizar uma instituição, e também
    detalha ou lista informações sobre uma ou mais instituições

    Campos:
        id: identificador (somente leitura)

        name: nome
    """

    class Meta:
        model = Institution
        fields = ["id", "name"]


class CampusCreateSerializer(ModelSerializer):
    """
    Recebe e valida informações para então cadastrar ou atualizar um campus

    Campos:
        id: identificador

        name: nome

        cnpj: cnpj

        address: endereço do campus

        number: número ou algo que identifique o local

        website: site do campus

        location: identificador da localização do campus

        institution: identificador da instituição
    """

    class Meta:
        model = Campus
        fields = [
            "id",
            "name",
            "cnpj",
            "address",
            "number",
            "website",
            "location",
            "institution",
        ]

    def validate_cnpj(self, cnpj):
        """
        Verifica se o cnpj é válido

        Argumentos:
            cnpj (str): atributo do serializer data

        Raises:
            ValidationError: caso o cnpj seja inválido

        Retorna:
            str: retorna o cnpj somente se for válido
        """
        if not CNPJ().validate(cnpj):
            raise ValidationError(CAMPUS_INVALID_CNPJ_MESSAGE)

        return cnpj


class CampusListSerializer(ModelSerializer):
    """
    Retorna uma lista de campi cadastrados no banco de dados

    Campos:
        id: identificador

        name: nome

        institution: informações sobre a instituição

        address: endereço do campus

        number: identificação do local
    """

    institution = InstitutionSerializer()

    class Meta:
        model = Campus
        fields = ["id", "name", "institution", "address", "number"]


class CampusDetailSerializer(ModelSerializer):
    """
    Retorna os detalhes de um campus específico

    Campos:
        id: identificador

        name: nome

        cnpj: cnpj

        address: endereço do campus

        number: identificação do local

        website: site do campus

        location: informações sobre a localização do campus

        institution: informações sobre a instituição
    """

    location = LocationSerializer()
    institution = InstitutionSerializer()

    class Meta:
        model = Campus
        fields = [
            "id",
            "name",
            "cnpj",
            "address",
            "number",
            "website",
            "location",
            "institution",
        ]
