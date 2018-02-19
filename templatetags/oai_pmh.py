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

from django.conf import settings
from django.template import Library
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from html import escape
from os import urandom

from ..models import MetadataFormat, ResumptionToken, Set
from ..settings import REPOSITORY_NAME


register = Library()


@register.filter
def get_item(d, key):
    return d[key] if key in d else None


@register.simple_tag
def admin_emails():
    admins = ['<adminEmail>%s</adminEmail>' % a[1] for a in settings.ADMINS]
    return mark_safe('\n'.join(admins))


@register.simple_tag
def base_url():
    url = settings.ALLOWED_HOSTS[0] if len(settings.ALLOWED_HOSTS) >= 1 else ''
    return '%s%s' % (url, reverse('oai2:oai2'))


@register.simple_tag
def list_request_attributes(verb=None, identifier=None, metadata_prefix=None,
                            from_timestamp=None, until_timestamp=None,
                            set_spec=None, resumption_token=None):
    timestamp_format = '%Y-%m-%dT%H:%M:%SZ'
    verbs = ['Identify', 'ListMetadataFormats', 'ListSets', 'GetRecord',
             'ListIdentifiers', 'ListRecords']

    attributes = ''
    if verb and verb in verbs:
        attributes = 'verb="%s"' % verb
    if identifier:
        attributes += ' identifier="%s"' % escape(identifier)
    if metadata_prefix:
        attributes += ' metadataPrefix="%s"' % escape(metadata_prefix)
    if from_timestamp:
        attributes += ' from="%s"' % from_timestamp.strftime(timestamp_format)
    if until_timestamp:
        attributes += ' until="%s"' % until_timestamp.strftime(timestamp_format)
    if set_spec:
        attributes += ' set="%s"' % escape(set_spec)
    if resumption_token:
        attributes += ' resumptionToken="%s"' % escape(resumption_token)
    return mark_safe(attributes)


@register.simple_tag
def multiple_tags(string, tag, delimiter=';'):
    tags = ['<%s>%s</%s>' % (tag, s, tag) for s in string.split(delimiter)]
    return mark_safe('\n'.join(tags))


@register.simple_tag
def repository_name():
    return mark_safe(REPOSITORY_NAME)


@register.simple_tag
def resumption_token(paginator, page, metadata_prefix=None, set_spec=None,
                     from_timestamp=None, until_timestamp=None):
    if paginator.num_pages > 0 and page.has_next():
        expiration_date = timezone.now() + timezone.timedelta(days=1)
        token = ''.join('%02x' % i for i in urandom(16))

        metadata_format = None
        if metadata_prefix:
            MetadataFormat.objects.get(prefix=metadata_prefix)
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
            until_timestamp=until_timestamp
        )

        tag = '<resumptionToken expirationDate="%s" completeListSize="%s" ' + \
            'cursor="%s">%s</resumptionToken>'
        return mark_safe(tag % (expiration_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                                paginator.count, page.end_index(), token))
    else:
        return ''


@register.simple_tag
def timestamp(format_string):
    if format_string == 'UTC':
        return timezone.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    return timezone.now().strftime(format_string)
