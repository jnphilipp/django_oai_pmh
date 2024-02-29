# Copyright (C) 2018-2024 J. Nathanael Philipp (jnphilipp) <nathanael@philipp.land>
#
# This file is part of django_oai_pmh.
#
# django_oai_pmh is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# django_oai_pmh is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with django_oai_pmh. If not, see <http://www.gnu.org/licenses/>.
# Generated by Django 2.0.2 on 2018-02-18 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("django_oai_pmh", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Set",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated at"),
                ),
                ("spec", models.TextField(unique=True, verbose_name="Spec")),
                ("name", models.TextField(verbose_name="Name")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Description"),
                ),
            ],
            options={
                "verbose_name": "Set",
                "verbose_name_plural": "Sets",
                "ordering": ("name",),
            },
        ),
    ]
