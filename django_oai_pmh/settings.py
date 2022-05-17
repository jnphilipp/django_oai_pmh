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
"""OAI-PMH Django app settings."""

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


USER_SETTINGS = getattr(settings, "OAI_PMH", {})

if "REPOSITORY_NAME" in USER_SETTINGS:
    REPOSITORY_NAME = USER_SETTINGS["REPOSITORY_NAME"]
else:
    raise ImproperlyConfigured("No value for REPOSITORY_NAME.")


if "BASE_URL" in USER_SETTINGS:
    BASE_URL = USER_SETTINGS["BASE_URL"]
else:
    raise ImproperlyConfigured("No value for BASE_URL.")

NUM_PER_PAGE = 100
if "NUM_PER_PAGE" in USER_SETTINGS:
    NUM_PER_PAGE = USER_SETTINGS["NUM_PER_PAGE"]
