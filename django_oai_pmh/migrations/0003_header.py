# -*- coding: utf-8 -*-
# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:
# Copyright (C) 2018-2022 J. Nathanael Philipp (jnphilipp) <nathanael@philipp.land>
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
# Generated by Django 2.0.2 on 2018-02-18 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("django_oai_pmh", "0002_set"),
    ]

    operations = [
        migrations.CreateModel(
            name="Header",
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
                (
                    "identifier",
                    models.TextField(unique=True, verbose_name="Identifier"),
                ),
                (
                    "timestamp",
                    models.DateTimeField(auto_now=True, verbose_name="Timestamp"),
                ),
                ("deleted", models.BooleanField(default=False, verbose_name="Deleted")),
                (
                    "metadata_formats",
                    models.ManyToManyField(
                        blank=True,
                        related_name="identifiers",
                        to="django_oai_pmh.MetadataFormat",
                        verbose_name="Metadata format",
                    ),
                ),
                (
                    "sets",
                    models.ManyToManyField(
                        blank=True,
                        related_name="headers",
                        to="django_oai_pmh.Set",
                        verbose_name="Set",
                    ),
                ),
            ],
            options={
                "verbose_name": "Header",
                "verbose_name_plural": "Headers",
                "ordering": ("identifier",),
            },
        ),
    ]
