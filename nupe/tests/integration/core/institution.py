from django.urls import reverse
from model_bakery import baker
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
)
from rest_framework.test import APITestCase

from nupe.core.models import Campus, Institution
from nupe.resources.datas.core.institution import CAMPUS_NAME, INSTITUTION_NAME, VALID_CNPJ
from nupe.tests.integration.account.setup.account import create_account_with_permissions_and_do_authentication


class InstitutionAPITestCase(APITestCase):
    def test_list_with_permission(self):
        # cria uma instituição no banco para retornar no list
        baker.make(Institution)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_institution"])
        url = reverse("institution-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados não mascarados do banco de dados
        self.assertEqual(response.data.get("count"), Institution.objects.count())

        data = response.data.get("results")[0]

        # campos que devem ser retornados
        self.assertIsNotNone(data.get("id"))
        self.assertIsNotNone(data.get("name"))

        # campos que não devem ser retornados
        self.assertIsNone(data.get("_safedelete_policy"))
        self.assertIsNone(data.get("campus"))

    def test_retrieve_with_permission(self):
        # cria uma instituição no banco para detalhar suas informações
        institution = baker.make(Institution)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_institution"])
        url = reverse("institution-detail", args=[institution.id])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações da instituição fornecida
        self.assertEqual(response.data.get("name"), institution.name)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("campus"))

    def test_create_with_permission(self):
        # instituição com informações válidas para conseguir criar
        institution_data = {"name": INSTITUTION_NAME}

        client = create_account_with_permissions_and_do_authentication(permissions=["core.add_institution"])
        url = reverse("institution-list")

        response = client.post(path=url, data=institution_data)

        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # deve ser criado no banco de dados
        self.assertEqual(Institution.objects.count(), 1)
        self.assertEqual(Institution.objects.all().first().name, INSTITUTION_NAME)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("name"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("campus"))

    def test_partial_update_with_permission(self):
        # cria uma instituição no banco para conseguir atualizar suas informações
        institution = baker.make(Institution)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.change_institution"])
        url = reverse("institution-detail", args=[institution.id])

        new_name = "name updated"
        institution_update_data = {
            "name": new_name,
        }

        response = client.patch(path=url, data=institution_update_data)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve ser atualizado no banco
        self.assertEqual(Institution.objects.get(pk=institution.id).name, new_name)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("name"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("campus"))

    def test_destroy_with_permission(self):
        # cria uma instituição no banco para conseguir excluir
        institution = baker.make(Institution)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.delete_institution"])
        url = reverse("institution-detail", args=[institution.id])

        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

        # o dado não deve ser removido nem mascarado
        self.assertEqual(Institution.objects.count(), 1)

    def test_list_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("institution-list")
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("institution-detail", args=[99])
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_create_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("institution-list")
        response = client.post(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_partial_update_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("institution-detail", args=[99])
        response = client.patch(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_destroy_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("institution-detail", args=[99])
        response = client.delete(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)


class CampusAPITestCase(APITestCase):
    def test_list_with_permission(self):
        # cria um campus no banco para retornar no list
        baker.make(Campus)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_campus"])
        url = reverse("campus-list")

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os dados não mascarados do banco de dados
        self.assertEqual(response.data.get("count"), Campus.objects.count())

        data = response.data.get("results")[0]

        # campos que devem ser retornados
        self.assertIsNotNone(data.get("id"))
        self.assertIsNotNone(data.get("name"))
        self.assertIsNotNone(data.get("institution"))
        self.assertIsNotNone(data.get("address"))
        self.assertIsNotNone(data.get("number"))

        # campos que não devem ser retornados
        self.assertIsNone(data.get("_safedelete_policy"))
        self.assertIsNone(data.get("cnpj"))
        self.assertIsNone(data.get("website"))
        self.assertIsNone(data.get("location"))
        self.assertIsNone(data.get("academic_education_campus"))
        self.assertIsNone(data.get("workers"))

    def test_retrieve_with_permission(self):
        # cria um campus no banco para detalhar suas informações
        campus = baker.make(Campus)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.view_campus"])
        url = reverse("campus-detail", args=[campus.id])

        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações do campus fornecido
        self.assertEqual(response.data.get("name"), campus.name)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("name"))
        self.assertIsNotNone(response.data.get("cnpj"))
        self.assertIsNotNone(response.data.get("address"))
        self.assertIsNotNone(response.data.get("number"))
        self.assertIsNot(response.data.get("website", False), False)
        self.assertIsNotNone(response.data.get("location"))
        self.assertIsNotNone(response.data.get("institution"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("academic_education_campus"))
        self.assertIsNone(response.data.get("workers"))

    def test_create_with_permission(self):
        # campus com informações válidas para conseguir criar
        campus_location = baker.make("core.Location")
        campus_institution = baker.make("core.Institution")

        campus_data = {
            "name": CAMPUS_NAME,
            "cnpj": VALID_CNPJ,
            "address": "someaddress",
            "number": "number11",
            "location": campus_location.id,
            "institution": campus_institution.id,
        }

        client = create_account_with_permissions_and_do_authentication(permissions=["core.add_campus"])
        url = reverse("campus-list")

        response = client.post(path=url, data=campus_data)

        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # deve ser criado no banco de dados
        campus = Campus.objects.all().first()
        self.assertEqual(Campus.objects.count(), 1)
        self.assertEqual(campus.name, CAMPUS_NAME)
        self.assertEqual(campus.cnpj, VALID_CNPJ)
        self.assertEqual(campus.address, "someaddress")
        self.assertEqual(campus.number, "number11")
        self.assertEqual(campus.location, campus_location)
        self.assertEqual(campus.institution, campus_institution)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("name"))
        self.assertIsNotNone(response.data.get("cnpj"))
        self.assertIsNotNone(response.data.get("address"))
        self.assertIsNotNone(response.data.get("number"))
        self.assertIsNot(response.data.get("website", False), False)
        self.assertIsNotNone(response.data.get("location"))
        self.assertIsNotNone(response.data.get("institution"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("academic_education_campus"))
        self.assertIsNone(response.data.get("workers"))

    def test_partial_update_with_permission(self):
        # cria um campus no banco para conseguir atualizar suas informações
        campus = baker.make(Campus)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.change_campus"])
        url = reverse("campus-detail", args=[campus.id])

        new_name = "name updated"
        campus_update_data = {
            "name": new_name,
        }

        response = client.patch(path=url, data=campus_update_data)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve ser atualizado no banco
        self.assertEqual(Campus.objects.get(pk=campus.id).name, new_name)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("id"))
        self.assertIsNotNone(response.data.get("name"))
        self.assertIsNotNone(response.data.get("cnpj"))
        self.assertIsNotNone(response.data.get("address"))
        self.assertIsNotNone(response.data.get("number"))
        self.assertIsNot(response.data.get("website", False), False)
        self.assertIsNotNone(response.data.get("location"))
        self.assertIsNotNone(response.data.get("institution"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("academic_education_campus"))
        self.assertIsNone(response.data.get("workers"))

    def test_destroy_with_permission(self):
        # cria um campus no banco para conseguir excluir
        campus = baker.make(Campus)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.delete_campus"])
        url = reverse("campus-detail", args=[campus.id])

        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

        # o dado não deve ser removido nem mascarado
        self.assertEqual(Campus.objects.count(), 1)

    def test_create_invalid_cnpj_with_permission(self):
        # campus com informações válidas para conseguir criar
        campus_location = baker.make("core.Location")
        campus_institution = baker.make("core.Institution")

        invalid_cnpj = "75775752000124"
        campus_data = {
            "name": CAMPUS_NAME,
            "cnpj": invalid_cnpj,
            "address": "someaddress",
            "number": "number11",
            "location": campus_location.id,
            "institution": campus_institution.id,
        }

        client = create_account_with_permissions_and_do_authentication(permissions=["core.add_campus"])
        url = reverse("campus-list")

        response = client.post(path=url, data=campus_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # não deve ser criado no banco de dados
        self.assertEqual(Campus.objects.count(), 0)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("cnpj"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("id"))
        self.assertIsNone(response.data.get("name"))
        self.assertIsNone(response.data.get("address"))
        self.assertIsNone(response.data.get("number"))
        self.assertIsNone(response.data.get("website"))
        self.assertIsNone(response.data.get("location"))
        self.assertIsNone(response.data.get("institution"))
        self.assertIsNone(response.data.get("academic_education_campus"))
        self.assertIsNone(response.data.get("workers"))

    def test_partial_update_invalid_cnpj_with_permission(self):
        # cria um campus no banco para conseguir atualizar suas informações
        campus = baker.make(Campus)

        client = create_account_with_permissions_and_do_authentication(permissions=["core.change_campus"])
        url = reverse("campus-detail", args=[campus.id])

        invalid_cnpj = "75775752000124"
        campus_update_data = {
            "cnpj": invalid_cnpj,
        }

        response = client.patch(path=url, data=campus_update_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # não deve ser atualizado no banco de dados
        self.assertNotEqual(Campus.objects.get(pk=campus.id).cnpj, invalid_cnpj)

        # campos que devem ser retornados
        self.assertIsNotNone(response.data.get("cnpj"))

        # campos que não devem ser retornados
        self.assertIsNone(response.data.get("_safedelete_policy"))
        self.assertIsNone(response.data.get("id"))
        self.assertIsNone(response.data.get("name"))
        self.assertIsNone(response.data.get("address"))
        self.assertIsNone(response.data.get("number"))
        self.assertIsNone(response.data.get("website"))
        self.assertIsNone(response.data.get("location"))
        self.assertIsNone(response.data.get("institution"))
        self.assertIsNone(response.data.get("academic_education_campus"))
        self.assertIsNone(response.data.get("workers"))

    def test_list_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("campus-list")
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("campus-detail", args=[99])
        response = client.get(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_create_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("campus-list")
        response = client.post(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_partial_update_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("campus-detail", args=[99])
        response = client.patch(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_destroy_without_permission(self):
        client = create_account_with_permissions_and_do_authentication()

        url = reverse("campus-detail", args=[99])
        response = client.delete(path=url)

        # não deve ter permissão para acessar
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
