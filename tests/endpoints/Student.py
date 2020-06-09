from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)
from rest_framework.test import APITestCase

from nupe.core.models import Student
from resources.const.datas.Person import CPF_2, RG_2
from resources.const.datas.Student import INGRESS_DATE, REGISTRATION
from tests.endpoints.setup.Person import create_person
from tests.endpoints.setup.Student import create_student
from tests.endpoints.setup.User import create_user_and_do_authentication
from tests.models.setup.Institution import create_academic_education_campus


class StudentAPITestCase(APITestCase):
    def test_list_student_with_permission(self):
        # cria um estudante no banco para retornar no list
        create_student()

        client = create_user_and_do_authentication(permissions=["core.view_student"])

        url = reverse("student-list")
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar todos os estudantes do banco de dados
        self.assertEqual(len(response.data), Student.objects.all().count())

    def test_retrieve_student_with_permission(self):
        # cria um estudante no banco para detalhar suas informações
        student = create_student()

        client = create_user_and_do_authentication(permissions=["core.view_student"])

        url = reverse("student-detail", args=[student.id])
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_200_OK)

        # deve retornar as informações do estudante do id fornecido
        self.assertEqual(response.data.get("id"), student.id)

    def test_create_student_with_permission(self):
        person1 = create_person()
        person2 = create_person(cpf=CPF_2, rg=RG_2)
        academic_education_campus = create_academic_education_campus()

        client = create_user_and_do_authentication(permissions=["core.add_student"])

        student = {
            "registration": REGISTRATION,
            "person": person1.id,
            "responsibles_persons": [person1.id, person2.id],
            "academic_education_campus": academic_education_campus.id,
            "ingress_date": INGRESS_DATE,
        }

        url = reverse("student-list")
        response = client.post(path=url, data=student)

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data.get("person"), person1.id)
        self.assertEqual(Student.objects.all().count(), 1)  # o estudante deve ser criado no banco de dados

    def test_partial_update_student_with_permission(self):
        # cria um estudante no banco para poder atualiza-lo
        student = create_student()

        client = create_user_and_do_authentication(permissions=["core.change_student"])

        new_registration = REGISTRATION + "1"
        student_data = {
            "registration": new_registration,
        }

        url = reverse("student-detail", args=[student.id])
        response = client.patch(path=url, data=student_data)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data.get("registration"), new_registration)

        # deve ser atualizado no banco
        self.assertEqual(Student.objects.get(id=student.id).registration, new_registration)

    def test_destroy_student_with_permission(self):
        # cria um estudante no banco para poder mascara-lo
        student = create_student()

        client = create_user_and_do_authentication(permissions=["core.delete_student"])

        url = reverse("student-detail", args=[student.id])
        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(Student.objects.all().count(), 0)  # deve ser mascarado
        self.assertEqual(Student.all_objects.all().count(), 1)  # mas deve ser mantido no banco de dados

    def test_create_invalid_student_with_permission(self):
        person1 = create_person()
        person2 = create_person(cpf=CPF_2, rg=RG_2)
        academic_education_campus = create_academic_education_campus()

        client = create_user_and_do_authentication(permissions=["core.add_student"])

        invalid_pk_academic_education_campus = 99
        student = {
            "registration": REGISTRATION,
            "person": person1.id,
            "responsibles_persons": [person1.id, person2.id],
            "academic_education_campus": invalid_pk_academic_education_campus,
            "ingress_date": INGRESS_DATE,
        }

        url = reverse("student-list")
        response = client.post(path=url, data=student)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # deve emitir mensagem de erro do campo inválido
        self.assertNotEqual(response.data.get("academic_education_campus"), None)

        invalid_pk_responsible = 99
        student = {
            "registration": REGISTRATION,
            "person": person1.id,
            "responsibles_persons": [person1.id, invalid_pk_responsible],
            "academic_education_campus": academic_education_campus.id,
            "ingress_date": INGRESS_DATE,
        }

        response = client.post(path=url, data=student)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.data.get("responsibles_persons"), None)

        invalid_pk_person = 99
        student = {
            "registration": REGISTRATION,
            "person": invalid_pk_person,
            "responsibles_persons": [person1.id, person2.id],
            "academic_education_campus": academic_education_campus.id,
            "ingress_date": INGRESS_DATE,
        }

        response = client.post(path=url, data=student)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.data.get("person"), None)

        invalid_registration = "teste"  # registration deve conter somente números
        student = {
            "registration": invalid_registration,
            "person": person1.id,
            "responsibles_persons": [person1.id, person2.id],
            "academic_education_campus": academic_education_campus.id,
            "ingress_date": INGRESS_DATE,
        }

        response = client.post(path=url, data=student)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.data.get("registration"), None)

        person1.birthday_date = "2005-06-10"
        person1.save()

        student = {
            "registration": "123",
            "person": person1.id,
            "responsibles_persons": [],
            "academic_education_campus": academic_education_campus.id,
            "ingress_date": INGRESS_DATE,
        }

        url = reverse("student-list")
        response = client.post(path=url, data=student)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # estudante menor de idade sem responsável deve emitir mensagem de erro do campo inválido
        self.assertNotEqual(response.data.get("responsibles_persons"), None)

    def test_partial_update_invalid_student_with_permission(self):
        # cria um estudante no banco para poder atualiza-lo
        student = create_student()

        client = create_user_and_do_authentication(permissions=["core.change_student"])

        invalid_registration = "invalid_registration"
        student_data = {
            "registration": invalid_registration,
        }

        url = reverse("student-detail", args=[student.id])
        response = client.patch(path=url, data=student_data)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.data.get("registration"), None)

    def test_list_student_without_permission(self):
        client = create_user_and_do_authentication(permissions=[])

        url = reverse("student-list")
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)  # não deve ter permissão para acessar

    def test_retrieve_student_without_permission(self):
        client = create_user_and_do_authentication(permissions=[])

        url = reverse("student-detail", args=[99])
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_create_student_without_permission(self):
        client = create_user_and_do_authentication(permissions=[])

        url = reverse("student-list")
        response = client.post(path=url, data={})

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_partial_update_student_without_permission(self):
        client = create_user_and_do_authentication(permissions=[])

        url = reverse("student-detail", args=[99])
        response = client.patch(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_destroy_student_without_permission(self):
        client = create_user_and_do_authentication(permissions=[])

        url = reverse("student-detail", args=[99])
        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_retrieve_id_not_found(self):
        client = create_user_and_do_authentication(permissions=["core.view_student"])

        url = reverse("student-detail", args=[99])  # qualquer id, o banco de dados para test é vazio
        response = client.get(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)  # não deve encontrar porque não existe

    def test_partial_update_id_not_found(self):
        client = create_user_and_do_authentication(permissions=["core.change_student"])

        url = reverse("student-detail", args=[99])
        response = client.patch(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_destroy_id_not_found(self):
        client = create_user_and_do_authentication(permissions=["core.delete_student"])

        url = reverse("student-detail", args=[99])
        response = client.delete(path=url)

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)