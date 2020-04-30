from django.core.exceptions import ValidationError
from django.test import TestCase

from nupe.core.models import COURSE_MAX_LENGTH, GRADE_MAX_LENGTH, AcademicEducation, Course, Grade

COURSE_NAME = "Informática"
GRADE_NAME = "Técnico"


class CourseTestCase(TestCase):
    def test_create_valid(self):
        course = Course.objects.create(name=COURSE_NAME)

        self.assertNotEqual(course.id, None)
        self.assertEqual(course.name, COURSE_NAME)
        self.assertEqual(Course.objects.all().count(), 1)
        self.assertEqual(course.full_clean(), None)

    def test_create_invalid_max_length(self):
        with self.assertRaises(ValidationError):
            Course(name=COURSE_NAME * COURSE_MAX_LENGTH).clean_fields()

    def test_create_invalid_null(self):
        with self.assertRaises(ValidationError):
            Course(name=None).clean_fields()

    def test_create_invalid_blank(self):
        with self.assertRaises(ValidationError):
            Course().clean_fields()

        with self.assertRaises(ValidationError):
            Course(name="").clean_fields()

        with self.assertRaises(ValidationError):
            Course(name=" ").clean_fields()

    def test_create_invalid_unique_name(self):
        with self.assertRaises(ValidationError):
            Course.objects.create(name=COURSE_NAME)
            Course(name=COURSE_NAME).validate_unique()


class GradeTestCase(TestCase):
    def test_create_valid(self):
        grade = Grade.objects.create(name=GRADE_NAME)

        self.assertNotEqual(grade.id, None)
        self.assertEqual(grade.name, GRADE_NAME)
        self.assertEqual(Grade.objects.all().count(), 1)
        self.assertEqual(grade.full_clean(), None)

    def test_create_invalid_max_length(self):
        with self.assertRaises(ValidationError):
            Grade(name=GRADE_NAME * GRADE_MAX_LENGTH).clean_fields()

    def test_create_invalid_null(self):
        with self.assertRaises(ValidationError):
            Grade(name=None).clean_fields()

    def test_create_invalid_blank(self):
        with self.assertRaises(ValidationError):
            Grade().clean_fields()

        with self.assertRaises(ValidationError):
            Grade(name="").clean_fields()

        with self.assertRaises(ValidationError):
            Grade(name=" ").clean_fields()

    def test_create_invalid_unique_name(self):
        with self.assertRaises(ValidationError):
            Grade.objects.create(name=GRADE_NAME)
            Grade(name=GRADE_NAME).validate_unique()


class AcademicEducationTestCase(TestCase):
    def setUp(self):
        Course.objects.create(name=COURSE_NAME)
        Grade.objects.create(name=GRADE_NAME)

    def test_create_valid(self):
        course = Course.objects.all().first()
        grade = Grade.objects.all().first()

        academic_education = AcademicEducation.objects.create(course=course, grade=grade)

        self.assertNotEqual(academic_education.id, None)
        self.assertEqual(academic_education.course, course)
        self.assertEqual(academic_education.grade, grade)
        self.assertEqual(AcademicEducation.objects.all().count(), 1)
        self.assertEqual(academic_education.full_clean(), None)

    def test_create_invalid_null(self):
        with self.assertRaises(ValidationError):
            AcademicEducation(course=None).clean_fields()

        with self.assertRaises(ValidationError):
            AcademicEducation(grade=None).clean_fields()

    def test_create_invalid_course_and_grade_instance(self):
        with self.assertRaises(ValueError):
            AcademicEducation(course="").clean_fields()

        with self.assertRaises(ValueError):
            AcademicEducation(grade="").clean_fields()

        with self.assertRaises(ValueError):
            AcademicEducation(course=1).clean_fields()

        with self.assertRaises(ValueError):
            AcademicEducation(grade=1).clean_fields()

    def test_create_invalid_course_and_grade_unique_together(self):
        course = Course.objects.all().first()
        grade = Grade.objects.all().first()

        with self.assertRaises(ValidationError):
            AcademicEducation.objects.create(course=course, grade=grade)
            AcademicEducation(course=course, grade=grade).validate_unique()
