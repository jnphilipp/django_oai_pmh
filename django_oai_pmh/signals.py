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
"""OAI-PMH Django app signals."""

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import ResumptionToken


@receiver(pre_save, sender=ResumptionToken)
def delete_old_resumption_tokens(sender, **kwargs):
    """Delete expired resumption tokens."""
    ResumptionToken.objects.filter(expiration_date__lte=timezone.now()).delete()
