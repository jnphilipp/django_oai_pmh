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
# Generated by Django 2.0.2 on 2018-02-18 21:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("django_oai_pmh", "0004_resumptiontoken"),
    ]

    operations = [
        migrations.CreateModel(
            name="DCRecord",
            fields=[
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated at"),
                ),
                (
                    "header",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="django_oai_pmh.header",
                        verbose_name="Header",
                    ),
                ),
                ("identifier", models.TextField(verbose_name=" dc:identifier")),
                ("date", models.DateTimeField(auto_now=True, verbose_name=" dc:date")),
                (
                    "title",
                    models.TextField(blank=True, null=True, verbose_name=" dc:title"),
                ),
                (
                    "creator",
                    models.TextField(blank=True, null=True, verbose_name=" dc:creator"),
                ),
                (
                    "subject",
                    models.TextField(blank=True, null=True, verbose_name=" dc:subject"),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, verbose_name=" dc:description"
                    ),
                ),
                (
                    "publisher",
                    models.TextField(
                        blank=True, null=True, verbose_name=" dc:publisher"
                    ),
                ),
                (
                    "contributor",
                    models.TextField(
                        blank=True, null=True, verbose_name=" dc:contributor"
                    ),
                ),
                (
                    "type",
                    models.TextField(blank=True, null=True, verbose_name=" dc:type"),
                ),
                (
                    "format",
                    models.TextField(blank=True, null=True, verbose_name=" dc:format"),
                ),
                (
                    "source",
                    models.TextField(blank=True, null=True, verbose_name=" dc:source"),
                ),
                (
                    "language",
                    models.TextField(
                        blank=True, null=True, verbose_name=" dc:language"
                    ),
                ),
                (
                    "relation",
                    models.TextField(
                        blank=True, null=True, verbose_name=" dc:relation"
                    ),
                ),
                (
                    "coverage",
                    models.TextField(
                        blank=True, null=True, verbose_name=" dc:coverage"
                    ),
                ),
                (
                    "rights",
                    models.TextField(blank=True, null=True, verbose_name=" dc:rights"),
                ),
            ],
            options={
                "verbose_name": "Dublin Core record",
                "verbose_name_plural": "Dublin Core records",
                "ordering": ("header",),
            },
        ),
    ]
