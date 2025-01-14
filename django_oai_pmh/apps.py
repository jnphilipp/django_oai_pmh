# Copyright (C) 2018-2025 J. Nathanael Philipp (jnphilipp) <nathanael@philipp.land>
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
"""OAI-PMH Django app config."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OAIPMHConfig(AppConfig):
    """OAI-PMH Django app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "django_oai_pmh"
    verbose_name = _("OAI-PMH")
    verbose_name_plural = _("OAI-PMH")

    def ready(self):
        """Ready."""
        from . import signals  # noqa: F401
