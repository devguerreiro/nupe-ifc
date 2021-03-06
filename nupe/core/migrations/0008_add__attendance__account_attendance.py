# Generated by Django 2.2.16 on 2020-10-09 18:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0007_add__attendance_reason"),
    ]

    operations = [
        migrations.CreateModel(
            name="AccountAttendance",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("deleted", models.DateTimeField(editable=False, null=True)),
                ("public_annotation", models.TextField(max_length="255", null=True, blank=True)),
                ("private_annotation", models.TextField(max_length="255", null=True, blank=True)),
                ("group_annotation", models.TextField(max_length="255", null=True, blank=True)),
                ("attendance_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="account_attendances",
                        related_query_name="account_attendance",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="Attendance",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("deleted", models.DateTimeField(editable=False, null=True)),
                (
                    "attendance_severity",
                    models.CharField(
                        choices=[("L", "Baixa"), ("M", "Média"), ("H", "Alta"), ("S", "Grave")],
                        help_text="Baixa = L, Média = M, Alta = H, Grave = S",
                        max_length=1,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("O", "Aberto"), ("OH", "Em Espera"), ("IP", "Em Atendimento"), ("C", "Fechado")],
                        default="O",
                        help_text="Aberto = O, Em Espero = OH, Em Andamento = IP, Fechado = C",
                        max_length=2,
                    ),
                ),
                ("opened_at", models.DateTimeField(auto_now_add=True)),
                ("closed_at", models.DateTimeField(blank=True, default=None, null=True)),
                (
                    "attendance_reason",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attendances",
                        related_query_name="attendance",
                        to="core.AttendanceReason",
                    ),
                ),
                (
                    "attendants",
                    models.ManyToManyField(
                        related_name="attendances",
                        related_query_name="attendance",
                        through="core.AccountAttendance",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="consultations",
                        related_query_name="consultation",
                        to="core.Student",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.AddField(
            model_name="accountattendance",
            name="attendance",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="account_attendances",
                related_query_name="account_attendance",
                to="core.Attendance",
            ),
        ),
    ]
