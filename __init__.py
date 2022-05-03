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
"""OAI-PMH Django app."""

__author__ = "J. Nathanael Philipp"
__copyright__ = "Copyright 2018-2022 J. Nathanael Philipp (jnphilipp)"
__license__ = "GPL"
__maintainer__ = __author__
__email__ = "nathanael@philipp.land"
__version__ = "0.1.2"
__version_info__ = tuple(int(part) for part in __version__.split("."))

default_app_config = "oai_pmh.apps.OAIPMHConfig"
