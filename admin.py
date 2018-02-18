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

from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .models import MetadataFormat, Set


@admin.register(MetadataFormat)
class MetadataFormatAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['prefix', 'schema', 'namespace']}),
    ]
    list_display = ('prefix', 'schema', 'namespace')
    search_fields = ('prefix', 'schema', 'namespace')


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'spec']}),
        (_('Description'), {'fields': ['description']}),
    ]
    list_display = ('name', 'spec', 'description')
    search_fields = ('name', 'spec', 'description')
