# -*- coding: utf-8 -*-
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
"""OAI-PMH Django app admin."""

from django.contrib import admin
from django.db import models
from django.forms.widgets import TextInput
from django.utils.translation import gettext_lazy as _

from .models import DCRecord, Header, MetadataFormat, ResumptionToken, Set, XMLRecord


@admin.register(DCRecord)
class DCRecordAdmin(admin.ModelAdmin):
    """DCRecord Django admin."""

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "created_at",
                    "updated_at",
                    "header",
                    "identifier",
                    "date",
                    "title",
                    "creator",
                    "subject",
                    "description",
                    "publisher",
                    "contributor",
                    "type",
                    "format",
                    "source",
                    "language",
                    "relation",
                    "coverage",
                    "rights",
                ]
            },
        ),
    ]
    formfield_overrides = {
        models.TextField: {"widget": TextInput},
    }
    list_display = ("identifier", "title", "creator", "date")
    list_filter = ("date",)
    readonly_fields = ("created_at", "updated_at", "date")
    search_fields = (
        "identifier",
        "title",
        "creator",
        "subject",
        "description",
        "publisher",
        "contributor",
        "date",
        "type",
        "format",
        "identifier",
        "source",
        "language",
        "relation",
        "coverage",
        "rights",
    )


@admin.register(Header)
class HeaderAdmin(admin.ModelAdmin):
    """Header Django admin."""

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "created_at",
                    "updated_at",
                    "identifier",
                    "timestamp",
                    "deleted",
                ]
            },
        ),
        (_("Metadata formats"), {"fields": ["metadata_formats"]}),
        (_("Sets"), {"fields": ["sets"]}),
    ]
    formfield_overrides = {
        models.TextField: {"widget": TextInput},
    }
    filter_horizontal = ("metadata_formats", "sets")
    list_display = ("identifier", "timestamp", "deleted")
    list_filter = ("timestamp", "deleted")
    readonly_fields = ("created_at", "updated_at", "timestamp")
    search_fields = ("identifier",)


@admin.register(MetadataFormat)
class MetadataFormatAdmin(admin.ModelAdmin):
    """MetadataFormat Django admin."""

    fieldsets = [
        (
            None,
            {"fields": ["created_at", "updated_at", "prefix", "schema", "namespace"]},
        ),
    ]
    formfield_overrides = {
        models.TextField: {"widget": TextInput},
    }
    list_display = ("prefix", "schema", "namespace")
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("prefix", "schema", "namespace")


@admin.register(ResumptionToken)
class ResumptionTokenAdmin(admin.ModelAdmin):
    """ResumptionToken Django admin."""

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "created_at",
                    "updated_at",
                    "token",
                    "expiration_date",
                    "complete_list_size",
                    "cursor",
                ]
            },
        ),
        (
            _("Optinal"),
            {
                "fields": [
                    "from_timestamp",
                    "until_timestamp",
                    "metadata_prefix",
                    "set_spec",
                ],
                "classes": ("collapse",),
            },
        ),
    ]
    formfield_overrides = {
        models.TextField: {"widget": TextInput},
    }
    list_display = ("token", "expiration_date", "complete_list_size", "cursor")
    list_filter = ("expiration_date",)
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("token", "complete_list_size", "cursor")


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    """Set Django admin."""

    fieldsets = [
        (None, {"fields": ["created_at", "updated_at", "name", "spec"]}),
        (_("Description"), {"fields": ["description"]}),
    ]
    formfield_overrides = {
        models.TextField: {"widget": TextInput},
    }
    list_display = ("name", "spec", "description")
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("name", "spec", "description")


@admin.register(XMLRecord)
class XMLRecordAdmin(admin.ModelAdmin):
    """XMLRecord Django admin."""

    fieldsets = [
        (None, {"fields": ["created_at", "updated_at", "header", "metadata_prefix"]}),
        (_("XML metadata"), {"fields": ["xml_metadata"]}),
    ]
    list_display = ("header", "metadata_prefix")
    readonly_fields = ("created_at", "updated_at")
    search_fields = (
        "header__identifier",
        "metadata_prefix__prefix",
        "metadata_prefix__schema",
    )
