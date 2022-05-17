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
"""OAI-PMH Django app models."""

import re

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _
from lxml import etree
from typing import Dict, List, Optional, Tuple, Type, TypeVar


class MetadataFormat(models.Model):
    """MetadataFormat Model."""

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    prefix = models.TextField(unique=True, verbose_name=_("Prefix"))
    schema = models.URLField(max_length=2048, verbose_name=_("Schema"))
    namespace = models.URLField(max_length=2048, verbose_name=_("Namespace"))

    def __str__(self):
        """Name."""
        return self.prefix

    class Meta:
        """Meta."""

        ordering = ("prefix",)
        verbose_name = _("Metadata format")
        verbose_name_plural = _("Metadata formats")


class Set(models.Model):
    """Set Model."""

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    spec = models.TextField(unique=True, verbose_name=_("Spec"))
    name = models.TextField(verbose_name=_("Name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))

    def __str__(self):
        """Name."""
        return self.name

    class Meta:
        """Meta."""

        ordering = ("name",)
        verbose_name = _("Set")
        verbose_name_plural = _("Sets")


class Header(models.Model):
    """Header Model."""

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    identifier = models.TextField(unique=True, verbose_name=_("Identifier"))
    timestamp = models.DateTimeField(auto_now=True, verbose_name=_("Timestamp"))
    deleted = models.BooleanField(default=False, verbose_name=_("Deleted"))
    metadata_formats = models.ManyToManyField(
        MetadataFormat,
        blank=True,
        related_name="identifiers",
        verbose_name=_("Metadata format"),
    )
    sets = models.ManyToManyField(
        Set,
        blank=True,
        related_name="headers",
        verbose_name=_("Set"),
    )

    def __str__(self):
        """Name."""
        return self.identifier

    class Meta:
        """Meta."""

        ordering = ("identifier",)
        verbose_name = _("Header")
        verbose_name_plural = _("Headers")


class ResumptionToken(models.Model):
    """ResumptionToken Model."""

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    expiration_date = models.DateTimeField(
        verbose_name=_("Expiration date"),
    )
    complete_list_size = models.IntegerField(
        default=0,
        verbose_name=_("Complete list size"),
    )
    cursor = models.IntegerField(default=0, verbose_name=_("Cursor"))
    token = models.TextField(unique=True, verbose_name=_("Token"))

    from_timestamp = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("From timestamp"),
    )
    until_timestamp = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Until timestamp"),
    )
    metadata_prefix = models.ForeignKey(
        MetadataFormat,
        models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("Metadata prefix"),
    )
    set_spec = models.ForeignKey(
        Set,
        models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("Set spec"),
    )

    def __str__(self):
        """Name."""
        return self.token

    class Meta:
        """Meta."""

        ordering = ("expiration_date",)
        verbose_name = _("Resumption token")
        verbose_name_plural = _("Resumption tokens")


class DCRecord(models.Model):
    """DCRecord Model."""

    T = TypeVar("T", bound="DCRecord", covariant=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    header = models.OneToOneField(
        Header, models.CASCADE, primary_key=True, verbose_name=_("Header")
    )

    title = ArrayField(models.TextField(verbose_name=" dc:title"), null=True)
    creator = ArrayField(models.TextField(verbose_name=" dc:creator"), null=True)
    subject = ArrayField(models.TextField(verbose_name=" dc:subject"), null=True)
    description = ArrayField(
        models.TextField(verbose_name=" dc:description"), null=True
    )
    publisher = ArrayField(models.TextField(verbose_name=" dc:publisher"), null=True)
    contributor = ArrayField(
        models.TextField(verbose_name=" dc:contributor"), null=True
    )
    date = ArrayField(models.TextField(verbose_name=" dc:date"), null=True)
    type = ArrayField(models.TextField(verbose_name=" dc:type"), null=True)
    format = ArrayField(models.TextField(verbose_name=" dc:format"), null=True)
    identifier = ArrayField(models.TextField(verbose_name=" dc:identifier"), null=True)
    source = ArrayField(models.TextField(verbose_name=" dc:source"), null=True)
    language = ArrayField(models.TextField(verbose_name=" dc:language"), null=True)
    relation = ArrayField(models.TextField(verbose_name=" dc:relation"), null=True)
    coverage = ArrayField(models.TextField(verbose_name=" dc:coverage"), null=True)
    rights = ArrayField(models.TextField(verbose_name=" dc:rights"), null=True)

    @classmethod
    def from_xml(cls: Type[T], data: str, header: Header) -> Tuple[Optional[T], bool]:
        """Create DCRecord from xml string."""
        defaults: Dict[str, List[str]] = {}
        for child in etree.XML(data):
            if not child.text:
                continue
            tag_name = re.sub(r"\{[^\}]+\}", "", child.tag)
            if tag_name not in defaults:
                defaults[tag_name] = []
            defaults[tag_name].append(child.text.strip())

        return cls.objects.update_or_create(header=header, defaults=defaults)

    def __str__(self: T) -> str:
        """Name."""
        return str(self.header)

    class Meta:
        """Meta."""

        ordering = ("header",)
        verbose_name = _("Dublin Core record")
        verbose_name_plural = _("Dublin Core records")


class XMLRecord(models.Model):
    """XMLRecord Model."""

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    header = models.ForeignKey(
        Header, models.CASCADE, related_name="xmlrecords", verbose_name=_("Header")
    )
    metadata_prefix = models.ForeignKey(
        MetadataFormat,
        models.CASCADE,
        related_name="xmlrecords",
        verbose_name=_("Metadata prefix"),
    )
    xml_metadata = models.TextField(verbose_name=_("XML metadta"))

    def save(self, *args, **kwargs):
        """Save."""
        self.xml_metadata = re.sub(r"^<\?xml[^>]+\?>\s*", "", self.xml_metadata)
        super(XMLRecord, self).save(*args, **kwargs)

    def __str__(self):
        """Name."""
        return f"{self.metadata_prefix}[{self.header}]"

    class Meta:
        """Meta."""

        ordering = ("header", "metadata_prefix")
        unique_together = ()
        verbose_name = _("XML record")
        verbose_name_plural = _("XML records")
