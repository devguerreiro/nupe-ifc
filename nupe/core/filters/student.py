from django_filters import CharFilter, DateFromToRangeFilter, FilterSet, NumberFilter

from nupe.core.models import Student


class StudentFilter(FilterSet):
    """
    Filtros para se utilizar nas requisições do endpoint de Student

    Exemplo:
        /api/v1/student?foo=xyz

        ou

        /api/v1/student?foo=xyz&bar=abc

    Parâmetros:
        ingress_date_before: menor a data fornecida (yyyy-mm-dd)

        ingress_date_after: maior a data fornecida (yyyy-mm-dd)

        academic_education: igual ao inteiro fornecido

        campus_name: igual a string fornecida (case insensitive)

        graduated: igual ao booleano fornecido (True, False)
    """

    ingress_date = DateFromToRangeFilter()
    academic_education = NumberFilter(field_name="academic_education_campus__academic_education")
    campus_name = CharFilter(field_name="academic_education_campus__campus__name", lookup_expr="iexact")

    class Meta:
        model = Student
        fields = ["graduated", "ingress_date", "academic_education", "campus_name"]
