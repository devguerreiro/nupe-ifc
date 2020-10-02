# Generated by Django 3.1 on 2020-10-02 19:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_add__function__sector"),
    ]

    operations = [
        migrations.CreateModel(
            name="AttendanceReason",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("deleted", models.DateTimeField(editable=False, null=True)),
                ("description", models.TextField(max_length=255)),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="CrisisType",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("deleted", models.DateTimeField(editable=False, null=True)),
                ("name", models.CharField(max_length=50, unique=True)),
                ("description", models.CharField(blank=True, max_length=150, null=True)),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="DrugType",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("deleted", models.DateTimeField(editable=False, null=True)),
                ("name", models.CharField(max_length=50, unique=True)),
                ("description", models.CharField(blank=True, max_length=150, null=True)),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="SpecialNeedType",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("deleted", models.DateTimeField(editable=False, null=True)),
                ("name", models.CharField(max_length=50, unique=True)),
                ("description", models.CharField(blank=True, max_length=150, null=True)),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="AttendanceReasonSpecialNeed",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("deleted", models.DateTimeField(editable=False, null=True)),
                (
                    "attendance_reason",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.attendancereason"),
                ),
                (
                    "special_need",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.specialneedtype"),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="AttendanceReasonDrug",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("deleted", models.DateTimeField(editable=False, null=True)),
                (
                    "attendance_reason",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.attendancereason"),
                ),
                ("drug", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.drugtype")),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="AttendanceReasonCrisis",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("deleted", models.DateTimeField(editable=False, null=True)),
                (
                    "attendance_reason",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.attendancereason"),
                ),
                ("crisis", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.crisistype")),
            ],
            options={"abstract": False,},
        ),
        migrations.AddField(
            model_name="attendancereason",
            name="crisis",
            field=models.ManyToManyField(
                related_name="attendances",
                related_query_name="attendance",
                through="core.AttendanceReasonCrisis",
                to="core.CrisisType",
            ),
        ),
        migrations.AddField(
            model_name="attendancereason",
            name="drug",
            field=models.ManyToManyField(
                related_name="attendances",
                related_query_name="attendance",
                through="core.AttendanceReasonDrug",
                to="core.DrugType",
            ),
        ),
        migrations.AddField(
            model_name="attendancereason",
            name="special_need",
            field=models.ManyToManyField(
                related_name="attendances",
                related_query_name="attendance",
                through="core.AttendanceReasonSpecialNeed",
                to="core.SpecialNeedType",
            ),
        ),
    ]
