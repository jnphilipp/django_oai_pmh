# -*- coding: utf-8 -*-
# Copyright (C) 2018-2021 J. Nathanael Philipp (jnphilipp) <nathanael@philipp.land>
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

import requests

from django.contrib.auth.models import AnonymousUser
from django.test import override_settings, RequestFactory, TestCase
from io import BytesIO, StringIO
from lxml import etree

from . import views


class IdentifyTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @override_settings(
        ADMINS=[('jnphilipp', 'nathanael@philipp.land')],
        ALLOWED_HOSTS=('test.com')
    )
    def test_identify(self):
        request = self.factory.get('/oai2?verb=Identify')
        request.user = AnonymousUser()
        response = views.oai2(request)
        self.assertEqual(response.status_code, 200)

        r = requests.get("http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd")
        self.assertEqual(r.status_code, 200)
        xmlschema = etree.XMLSchema(etree.parse(StringIO(r.text)))
        doc = etree.parse(BytesIO(response.content))
        self.assertTrue(xmlschema.validate(doc))

    @override_settings(
        ADMINS=[('jnphilipp', 'nathanael@philipp.land')],
        ALLOWED_HOSTS=('test.com')
    )
    def test_identify_with_error(self):
        request = self.factory.get('/oai2?verb=Identify2')
        request.user = AnonymousUser()
        response = views.oai2(request)
        self.assertEqual(response.status_code, 200)

        r = requests.get("http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd")
        self.assertEqual(r.status_code, 200)
        xmlschema = etree.XMLSchema(etree.parse(StringIO(r.text)))
        doc = etree.parse(BytesIO(response.content))
        self.assertTrue(xmlschema.validate(doc))


class ListMetadataFormatsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @override_settings(
        ADMINS=[('jnphilipp', 'nathanael@philipp.land')],
        ALLOWED_HOSTS=('test.com')
    )
    def test_identify(self):
        request = self.factory.get('/oai2?verb=ListMetadataFormats&identifier=oai_dc')
        request.user = AnonymousUser()
        response = views.oai2(request)
        self.assertEqual(response.status_code, 200)

        r = requests.get("http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd")
        self.assertEqual(r.status_code, 200)
        xmlschema = etree.XMLSchema(etree.parse(StringIO(r.text)))
        doc = etree.parse(BytesIO(response.content))
        self.assertTrue(xmlschema.validate(doc))

    @override_settings(
        ADMINS=[('jnphilipp', 'nathanael@philipp.land')],
        ALLOWED_HOSTS=('test.com')
    )
    def test_identify_with_error(self):
        request = self.factory.get('/oai2?verb=ListMetadataFormats')
        request.user = AnonymousUser()
        response = views.oai2(request)
        self.assertEqual(response.status_code, 200)

        r = requests.get("http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd")
        self.assertEqual(r.status_code, 200)
        xmlschema = etree.XMLSchema(etree.parse(StringIO(r.text)))
        doc = etree.parse(BytesIO(response.content))
        self.assertTrue(xmlschema.validate(doc))
        self.assertTrue()
