# Copyright (C) 2018-2026 J. Nathanael Philipp (jnphilipp) <nathanael@philipp.land>
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

import re
import requests

from django.contrib.auth.models import AnonymousUser
from django.test import override_settings, RequestFactory, TestCase
from io import BytesIO, StringIO
from lxml import etree

from . import views
from .models import DCRecord, Header, MetadataFormat, Set, XMLRecord


OAI_DC_RECORD = """<?xml version="1.0"?>
<oai_dc:dc xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
  <dc:title xml:lang="en-US">Time course and hazard function: A distributional analysis of fixation duration in reading</dc:title>
  <dc:creator>Feng, Gary</dc:creator>
  <dc:description xml:lang="en-US">Reading processes affect not only the mean of fixation duration but also its distribution function. This paper introduces a set of hypotheses that link the timing and strength of a reading process to the hazard function of a fixation duration distribution. Analyses based on large corpora of reading eye movements show a surprisingly robust hazard function across languages, age, individual differences, and a number of processing variables. The data suggest that eye movements are generated stochastically based on a stereotyped time course that is independent of reading variables. High-level reading processes, however, modulate eye movement programming by increasing or decreasing the momentary saccade rate during a narrow time window. Implications to theories and analyses of reading eye movement are discussed.PS: The author wishes to thank Alan Kennedy for sharing the Dundee English reading eye movement corpus. See the Methods and References sections in the article for more details.</dc:description>
  <dc:publisher xml:lang="en-US">The Mind Research Repository (beta)</dc:publisher>
  <dc:date>2013-03-17</dc:date>
  <dc:type>info:eu-repo/semantics/article</dc:type>
  <dc:type>info:eu-repo/semantics/publishedVersion</dc:type>
  <dc:format>application/pdf</dc:format>
  <dc:identifier>11022/0000-0000-1F0B-3</dc:identifier>
  <dc:source xml:lang="en-US">The Mind Research Repository (beta); No 1 (2013)</dc:source>
  <dc:language>eng</dc:language>
  <dc:relation>https://repo.data.saw-leipzig.de/resources?identifier=mrr/11022000000001F0B3/Feng2009_1.0.tar.gz</dc:relation>
  <dc:relation>https://repo.data.saw-leipzig.de/resources?identifier=mrr/11022000000001F0B3/paper.pdf</dc:relation>
  <dc:relation>https://repo.data.saw-leipzig.de/resources?identifier=mrr/11022000000001F0B3</dc:relation>
</oai_dc:dc>"""


class DCRecordTestCase(TestCase):
    def test_from_xml(self):
        header = Header.objects.create(identifier="test:1")
        header.metadata_formats.add(MetadataFormat.objects.get(prefix="oai_dc"))

        dc_record, created = DCRecord.from_xml(
            OAI_DC_RECORD,
            header,
        )
        self.assertTrue(created)

        self.assertEqual(
            [
                "Time course and hazard function: A distributional analysis of fixation "
                + "duration in reading"
            ],
            dc_record.title,
        )
        self.assertEqual(["Feng, Gary"], dc_record.creator)
        self.assertEqual(
            [
                "Reading processes affect not only the mean of fixation duration but also its distribution function. This paper introduces a set of hypotheses that link the timing and strength of a reading process to the hazard function of a fixation duration distribution. Analyses based on large corpora of reading eye movements show a surprisingly robust hazard function across languages, age, individual differences, and a number of processing variables. The data suggest that eye movements are generated stochastically based on a stereotyped time course that is independent of reading variables. High-level reading processes, however, modulate eye movement programming by increasing or decreasing the momentary saccade rate during a narrow time window. Implications to theories and analyses of reading eye movement are discussed.PS: The author wishes to thank Alan Kennedy for sharing the Dundee English reading eye movement corpus. See the Methods and References sections in the article for more details."
            ],
            dc_record.description,
        )
        self.assertEqual(["The Mind Research Repository (beta)"], dc_record.publisher)
        self.assertEqual(["2013-03-17"], dc_record.date)
        self.assertEqual(
            [
                "info:eu-repo/semantics/article",
                "info:eu-repo/semantics/publishedVersion",
            ],
            dc_record.type,
        )
        self.assertEqual(["application/pdf"], dc_record.format)
        self.assertEqual(["11022/0000-0000-1F0B-3"], dc_record.identifier)
        self.assertEqual(
            ["The Mind Research Repository (beta); No 1 (2013)"], dc_record.source
        )
        self.assertEqual(["eng"], dc_record.language)
        self.assertEqual(
            [
                "https://repo.data.saw-leipzig.de/resources?identifier=mrr/11022000000001F0B3/Feng2009_1.0.tar.gz",
                "https://repo.data.saw-leipzig.de/resources?identifier=mrr/11022000000001F0B3/paper.pdf",
                "https://repo.data.saw-leipzig.de/resources?identifier=mrr/11022000000001F0B3",
            ],
            dc_record.relation,
        )


class XMLRecordTestCase(TestCase):
    def test_from_xml(self):
        oai_dc = MetadataFormat.objects.get(prefix="oai_dc")
        header = Header.objects.create(identifier="test:1")
        header.metadata_formats.add(oai_dc)

        xml_record = XMLRecord.objects.create(
            xml_metadata=OAI_DC_RECORD, header=header, metadata_prefix=oai_dc
        )
        self.assertIsNotNone(xml_record)
        self.assertIsNotNone(xml_record.pk)


class IdentifyTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @override_settings(
        ADMINS=[("jnphilipp", "nathanael@philipp.land")], ALLOWED_HOSTS=("test.com")
    )
    def test_identify(self):
        request = self.factory.get("/oai2?verb=Identify")
        request.user = AnonymousUser()
        response = views.oai2(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(
            re.search(
                r"<error code[^>]+>[^<]+</error>", response.content.decode("utf8")
            )
        )

        r = requests.get("http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd")
        self.assertEqual(r.status_code, 200)
        xmlschema = etree.XMLSchema(etree.parse(StringIO(r.text)))
        doc = etree.parse(BytesIO(response.content))
        self.assertTrue(xmlschema.validate(doc))

    @override_settings(
        ADMINS=[("jnphilipp", "nathanael@philipp.land")], ALLOWED_HOSTS=("test.com")
    )
    def test_identify_with_error(self):
        request = self.factory.get("/oai2?verb=Identify2")
        request.user = AnonymousUser()
        response = views.oai2(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(
            re.search(
                r"<error code=\"badVerb\">[^<]+</error>",
                response.content.decode("utf8"),
            )
        )

        r = requests.get("http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd")
        self.assertEqual(r.status_code, 200)
        xmlschema = etree.XMLSchema(etree.parse(StringIO(r.text)))
        doc = etree.parse(BytesIO(response.content))
        self.assertTrue(xmlschema.validate(doc))


class ListMetadataFormatsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @override_settings(
        ADMINS=[("jnphilipp", "nathanael@philipp.land")], ALLOWED_HOSTS=("test.com")
    )
    def test_list(self):
        request = self.factory.get("/oai2?verb=ListMetadataFormats")
        request.user = AnonymousUser()
        response = views.oai2(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(
            re.search(
                r"<error code[^>]+>[^<]+</error>", response.content.decode("utf8")
            )
        )

        r = requests.get("http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd")
        self.assertEqual(r.status_code, 200)
        xmlschema = etree.XMLSchema(etree.parse(StringIO(r.text)))
        doc = etree.parse(BytesIO(response.content))
        self.assertTrue(xmlschema.validate(doc))

    @override_settings(
        ADMINS=[("jnphilipp", "nathanael@philipp.land")], ALLOWED_HOSTS=("test.com")
    )
    def test_list_with_error(self):
        request = self.factory.get("/oai2?verb=ListMetadataFormats&identifier=oai:1")
        request.user = AnonymousUser()
        response = views.oai2(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(
            re.search(
                r"<error code=\"idDoesNotExist\">[^<]+</error>",
                response.content.decode("utf8"),
            )
        )

        r = requests.get("http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd")
        self.assertEqual(r.status_code, 200)
        xmlschema = etree.XMLSchema(etree.parse(StringIO(r.text)))
        doc = etree.parse(BytesIO(response.content))
        self.assertTrue(xmlschema.validate(doc))


class ListIdentifiersTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @override_settings(
        ADMINS=[("jnphilipp", "nathanael@philipp.land")], ALLOWED_HOSTS=("test.com")
    )
    def test_list(self):
        for i in range(10):
            header = Header.objects.create(identifier=f"oai:{i}")
            header.metadata_formats.add(MetadataFormat.objects.get(prefix="oai_dc"))

        request = self.factory.get("/oai2?verb=ListIdentifiers&metadataPrefix=oai_dc")
        request.user = AnonymousUser()
        response = views.oai2(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(
            re.search(
                r"<error code[^>]+>[^<]+</error>", response.content.decode("utf8")
            )
        )

        r = requests.get("http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd")
        self.assertEqual(r.status_code, 200)
        xmlschema = etree.XMLSchema(etree.parse(StringIO(r.text)))
        doc = etree.parse(BytesIO(response.content))
        self.assertTrue(xmlschema.validate(doc))

    @override_settings(
        ADMINS=[("jnphilipp", "nathanael@philipp.land")], ALLOWED_HOSTS=("test.com")
    )
    def test_list_with_resumption_token(self):
        for i in range(300):
            header = Header.objects.create(identifier=f"oai:{i}")
            header.metadata_formats.add(MetadataFormat.objects.get(prefix="oai_dc"))

        request = self.factory.get("/oai2?verb=ListIdentifiers&metadataPrefix=oai_dc")
        request.user = AnonymousUser()
        response = views.oai2(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(
            re.search(
                r"<error code[^>]+>[^<]+</error>", response.content.decode("utf8")
            )
        )

        r = requests.get("http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd")
        self.assertEqual(r.status_code, 200)
        xmlschema = etree.XMLSchema(etree.parse(StringIO(r.text)))
        doc = etree.parse(BytesIO(response.content))
        self.assertTrue(xmlschema.validate(doc))

        token = None
        match = re.search(
            r"<resumptionToken[^>]+>(?P<token>[^<]+)</resumptionToken>",
            response.content.decode("utf8"),
        )
        if match:
            token = match.group("token")

        request = self.factory.get(
            f"/oai2?verb=ListIdentifiers&resumptionToken={token}"
        )
        request.user = AnonymousUser()
        response = views.oai2(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(
            re.search(
                r"<error code[^>]+>[^<]+</error>", response.content.decode("utf8")
            )
        )

        r = requests.get("http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd")
        self.assertEqual(r.status_code, 200)
        xmlschema = etree.XMLSchema(etree.parse(StringIO(r.text)))
        doc = etree.parse(BytesIO(response.content))
        self.assertTrue(xmlschema.validate(doc))

    @override_settings(
        ADMINS=[("jnphilipp", "nathanael@philipp.land")], ALLOWED_HOSTS=("test.com")
    )
    def test_list_with_error(self):
        for i in range(10):
            Header.objects.create(identifier=f"oai:{i}")

        request = self.factory.get("/oai2?verb=ListIdentifiers&metadataPrefix=oai_dc")
        request.user = AnonymousUser()
        response = views.oai2(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(
            re.search(
                r"<error code=\"noRecordsMatch\">[^<]+</error>",
                response.content.decode("utf8"),
            )
        )

        r = requests.get("http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd")
        self.assertEqual(r.status_code, 200)
        xmlschema = etree.XMLSchema(etree.parse(StringIO(r.text)))
        doc = etree.parse(BytesIO(response.content))
        self.assertTrue(xmlschema.validate(doc))

        request = self.factory.get("/oai2?verb=ListIdentifiers&resumptionToken=fsahfk")
        request.user = AnonymousUser()
        response = views.oai2(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(
            re.search(
                r"<error code=\"badResumptionToken\">[^<]+</error>",
                response.content.decode("utf8"),
            )
        )

        r = requests.get("http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd")
        self.assertEqual(r.status_code, 200)
        xmlschema = etree.XMLSchema(etree.parse(StringIO(r.text)))
        doc = etree.parse(BytesIO(response.content))
        self.assertTrue(xmlschema.validate(doc))


class ListSetTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @override_settings(
        ADMINS=[("jnphilipp", "nathanael@philipp.land")], ALLOWED_HOSTS=("test.com")
    )
    def test_list(self):
        for i in range(10):
            Set.objects.create(spec=f"oai:{i}", name=f"{i}")

        request = self.factory.get("/oai2?verb=ListSets")
        request.user = AnonymousUser()
        response = views.oai2(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(
            re.search(
                r"<error code[^>]+>[^<]+</error>", response.content.decode("utf8")
            )
        )

        r = requests.get("http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd")
        self.assertEqual(r.status_code, 200)
        xmlschema = etree.XMLSchema(etree.parse(StringIO(r.text)))
        doc = etree.parse(BytesIO(response.content))
        self.assertTrue(xmlschema.validate(doc))

    @override_settings(
        ADMINS=[("jnphilipp", "nathanael@philipp.land")], ALLOWED_HOSTS=("test.com")
    )
    def test_list_with_resumption_token(self):
        for i in range(300):
            Set.objects.create(spec=f"oai:{i}", name=f"{i}")

        request = self.factory.get("/oai2?verb=ListSets")
        request.user = AnonymousUser()
        response = views.oai2(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(
            re.search(
                r"<error code[^>]+>[^<]+</error>", response.content.decode("utf8")
            )
        )

        r = requests.get("http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd")
        self.assertEqual(r.status_code, 200)
        xmlschema = etree.XMLSchema(etree.parse(StringIO(r.text)))
        doc = etree.parse(BytesIO(response.content))
        self.assertTrue(xmlschema.validate(doc))

        token = None
        match = re.search(
            r"<resumptionToken[^>]+>(?P<token>[^<]+)</resumptionToken>",
            response.content.decode("utf8"),
        )
        if match:
            token = match.group("token")

        request = self.factory.get(f"/oai2?verb=ListSets&resumptionToken={token}")
        request.user = AnonymousUser()
        response = views.oai2(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(
            re.search(
                r"<error code[^>]+>[^<]+</error>", response.content.decode("utf8")
            )
        )

        r = requests.get("http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd")
        self.assertEqual(r.status_code, 200)
        xmlschema = etree.XMLSchema(etree.parse(StringIO(r.text)))
        doc = etree.parse(BytesIO(response.content))
        self.assertTrue(xmlschema.validate(doc))

    @override_settings(
        ADMINS=[("jnphilipp", "nathanael@philipp.land")], ALLOWED_HOSTS=("test.com")
    )
    def test_list_with_error(self):
        request = self.factory.get("/oai2?verb=ListSets")
        request.user = AnonymousUser()
        response = views.oai2(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(
            re.search(
                r"<error code=\"noSetHierarchy\">[^<]+</error>",
                response.content.decode("utf8"),
            )
        )

        r = requests.get("http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd")
        self.assertEqual(r.status_code, 200)
        xmlschema = etree.XMLSchema(etree.parse(StringIO(r.text)))
        doc = etree.parse(BytesIO(response.content))
        self.assertTrue(xmlschema.validate(doc))

        for i in range(10):
            Set.objects.create(spec=f"oai:{i}", name=f"{i}")

        request = self.factory.get("/oai2?verb=ListSets&resumptionToken=fsahfk")
        request.user = AnonymousUser()
        response = views.oai2(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(
            re.search(
                r"<error code=\"badResumptionToken\">[^<]+</error>",
                response.content.decode("utf8"),
            )
        )

        r = requests.get("http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd")
        self.assertEqual(r.status_code, 200)
        xmlschema = etree.XMLSchema(etree.parse(StringIO(r.text)))
        doc = etree.parse(BytesIO(response.content))
        self.assertTrue(xmlschema.validate(doc))


class GetRecordTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        oai_dc = MetadataFormat.objects.get(prefix="oai_dc")

        self.header1 = Header.objects.create(identifier="test:1")
        self.header1.metadata_formats.add(oai_dc)

        self.dc_record, created = DCRecord.from_xml(
            OAI_DC_RECORD,
            self.header1,
        )

        self.header2 = Header.objects.create(identifier="test:2")
        self.header2.metadata_formats.add(oai_dc)
        self.xml_record = XMLRecord.objects.create(
            xml_metadata=OAI_DC_RECORD, header=self.header2, metadata_prefix=oai_dc
        )

    @override_settings(
        ADMINS=[("jnphilipp", "nathanael@philipp.land")], ALLOWED_HOSTS=("test.com")
    )
    def test_get_record(self):
        request = self.factory.get(
            "/oai2?verb=GetRecord&identifier=test:1&metadataPrefix=oai_dc"
        )
        request.user = AnonymousUser()
        response = views.oai2(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(
            re.search(
                r"<error code[^>]+>[^<]+</error>", response.content.decode("utf8")
            )
        )

        request = self.factory.get(
            "/oai2?verb=GetRecord&identifier=test:2&metadataPrefix=oai_dc"
        )
        request.user = AnonymousUser()
        response = views.oai2(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(
            re.search(
                r"<error code[^>]+>[^<]+</error>", response.content.decode("utf8")
            )
        )
        self.assertTrue(
            OAI_DC_RECORD[OAI_DC_RECORD.index("\n") + 1 :]
            in response.content.decode("utf8")
        )
