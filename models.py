# -*- coding: utf-8 -*-
# Copyright (C) 2018 Nathanael Philipp (jnphilipp) <mail@jnphilipp.org>
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

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .fields import SingleLineTextField


class MetadataFormat(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    prefix = SingleLineTextField(unique=True)
    schema = models.URLField(max_length=2048)
    namespace = models.URLField(max_length=2048)

    def __str__(self):
        return self.prefix

    class Meta:
        ordering = ('prefix',)
        verbose_name = _('Metadata format')
        verbose_name_plural = _('Metadata formats')


class Set(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    spec = SingleLineTextField(unique=True)
    name = SingleLineTextField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = _('Set')
        verbose_name_plural = _('Sets')


class Header(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    identifier = SingleLineTextField(unique=True)
    timestamp = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    metadata_formats = models.ManyToManyField(
        MetadataFormat,
        blank=True,
        related_name='identifiers'
    )
    sets = models.ManyToManyField(
        Set,
        blank=True,
        related_name='headers'
    )

    def __str__(self):
        return self.identifier

    class Meta:
        ordering = ('identifier',)
        verbose_name = _('Header')
        verbose_name_plural = _('Headers')


class ResumptionToken(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    expiration_date = models.DateTimeField()
    complete_list_size = models.IntegerField(default=0)
    cursor = models.IntegerField(default=0)
    token = SingleLineTextField(unique=True)

    from_timestamp = models.DateTimeField(blank=True, null=True)
    until_timestamp = models.DateTimeField(blank=True, null=True)
    metadata_prefix = models.ForeignKey(
        MetadataFormat,
        models.CASCADE,
        blank=True,
        null=True
    )
    set_spec = models.ForeignKey(
        Set,
        models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.token

    class Meta:
        ordering = ('expiration_date',)
        verbose_name = _('Resumption token')
        verbose_name_plural = _('Resumption tokens')


class DCRecord(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    header = models.OneToOneField(Header, models.CASCADE, primary_key=True)
    identifier = SingleLineTextField(verbose_name=' dc:identifier')
    date = models.DateTimeField(auto_now=True, verbose_name=' dc:date')
    title = SingleLineTextField(
        blank=True,
        null=True,
        verbose_name=' dc:title'
    )
    creator = SingleLineTextField(
        blank=True,
        null=True,
        verbose_name=' dc:creator'
    )
    subject = SingleLineTextField(
        blank=True,
        null=True,
        verbose_name=' dc:subject'
    )
    description = SingleLineTextField(
        blank=True,
        null=True,
        verbose_name=' dc:description'
    )
    publisher = SingleLineTextField(
        blank=True,
        null=True,
        verbose_name=' dc:publisher'
    )
    contributor = SingleLineTextField(
        blank=True,
        null=True,
        verbose_name=' dc:contributor'
    )
    type = SingleLineTextField(
        blank=True,
        null=True,
        verbose_name=' dc:type'
    )
    format = SingleLineTextField(
        blank=True,
        null=True,
        verbose_name=' dc:format'
    )
    source = SingleLineTextField(
        blank=True,
        null=True,
        verbose_name=' dc:source'
    )
    language = SingleLineTextField(
        blank=True,
        null=True,
        verbose_name=' dc:language'
    )
    relation = SingleLineTextField(
        blank=True,
        null=True,
        verbose_name=' dc:relation'
    )
    coverage = SingleLineTextField(
        blank=True,
        null=True,
        verbose_name=' dc:coverage'
    )
    rights = SingleLineTextField(
        blank=True,
        null=True,
        verbose_name=' dc:rights'
    )

    def __str__(self):
        return str(self.header)

    class Meta:
        ordering = ('header',)
        verbose_name = _('Dublin Core record')
        verbose_name_plural = _('Dublin Core records')
