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
"""OAI-PMH Django app oai_pmh templatetag."""

from django.conf import settings
from django.template import Library
from django.utils import timezone
from django.utils.safestring import mark_safe
from html import escape
from os import urandom

from ..models import MetadataFormat, ResumptionToken, Set
from ..settings import REPOSITORY_NAME, BASE_URL


register = Library()


@register.filter
def has_xmlrecord(header, metadata_prefix) -> bool:
    """Check whether header has XMLRecord with metadata prefix."""
    return header.xmlrecords.filter(metadata_prefix__prefix=metadata_prefix).exists()


@register.filter
def xmlrecord(header, metadata_prefix):
    """Check whether header has XMLRecord with metadata prefix."""
    return mark_safe(
        header.xmlrecords.get(metadata_prefix__prefix=metadata_prefix).xml_metadata
    )


@register.simple_tag
def admin_emails():
    """Format ADMINS for adminEmail-tag."""
    return mark_safe(
        "\n".join([f"<adminEmail>{admin[1]}</adminEmail>" for admin in settings.ADMINS])
    )


@register.simple_tag
def base_url():
    """Get OAI-PMH base url."""
    return mark_safe(BASE_URL)


@register.simple_tag
def list_request_attributes(
    verb=None,
    identifier=None,
    metadata_prefix=None,
    from_timestamp=None,
    until_timestamp=None,
    set_spec=None,
    resumption_token=None,
):
    """List requested attributes."""
    timestamp_format = "%Y-%m-%dT%H:%M:%SZ"
    verbs = [
        "Identify",
        "ListMetadataFormats",
        "ListSets",
        "GetRecord",
        "ListIdentifiers",
        "ListRecords",
    ]

    attributes = ""
    if verb and verb in verbs:
        attributes = f'verb="{verb}"'
    if identifier:
        attributes += f' identifier="{escape(identifier)}"'
    if metadata_prefix:
        attributes += f' metadataPrefix="{escape(metadata_prefix)}"'
    if from_timestamp:
        attributes += f' from="{from_timestamp.strftime(timestamp_format)}"'
    if until_timestamp:
        attributes += f' until="{until_timestamp.strftime(timestamp_format)}"'
    if set_spec:
        attributes += f' set="{escape(set_spec)}"'
    if resumption_token:
        attributes += f' resumptionToken="{escape(resumption_token)}"'
    return mark_safe(attributes)


@register.simple_tag
def repository_name():
    """Format repository name."""
    return mark_safe(REPOSITORY_NAME)


@register.simple_tag
def resumption_token(
    paginator,
    page,
    metadata_prefix=None,
    set_spec=None,
    from_timestamp=None,
    until_timestamp=None,
):
    """Get resumption token."""
    if paginator.num_pages > 0 and page.has_next():
        expiration_date = timezone.now() + timezone.timedelta(days=1)
        token = "".join("%02x" % i for i in urandom(16))

        metadata_format = None
        if metadata_prefix:
            metadata_format = MetadataFormat.objects.get(prefix=metadata_prefix)
        set_spec = None
        if set_spec:
            set_spec = Set.objects.get(spec=set_spec)

        ResumptionToken.objects.create(
            token=token,
            expiration_date=expiration_date,
            complete_list_size=paginator.count,
            cursor=page.end_index(),
            metadata_prefix=metadata_format,
            set_spec=set_spec,
            from_timestamp=from_timestamp,
            until_timestamp=until_timestamp,
        )

        return mark_safe(
            "<resumptionToken expirationDate="
            + f"\"{expiration_date.strftime('%Y-%m-%dT%H:%M:%SZ')}\" "
            + f'completeListSize="{paginator.count}" cursor="{page.end_index()}">'
            + f"{token}</resumptionToken>"
        )
    else:
        return ""
