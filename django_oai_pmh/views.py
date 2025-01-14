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
"""OAI-PMH Django app views."""

from datetime import datetime
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import Header, MetadataFormat, Set, ResumptionToken
from .settings import NUM_PER_PAGE


@csrf_exempt
def oai2(request):
    """Handels all OAI-PMH v2 requets.

    For details see https://www.openarchives.org/OAI/openarchivesprotocol.html
    """
    params = request.POST.copy() if request.method == "POST" else request.GET.copy()

    errors = []
    verb = None
    identifier = None
    metadata_prefix = None
    set_spec = None
    from_timestamp = None
    until_timestamp = None
    resumption_token = None

    if "verb" in params:
        verb = params.pop("verb")[-1]
        if verb == "GetRecord":
            template = "django_oai_pmh/getrecord.xml"

            if "metadataPrefix" in params:
                metadata_prefix = params.pop("metadataPrefix")
                if len(metadata_prefix) == 1:
                    metadata_prefix = metadata_prefix[0]
                    if not MetadataFormat.objects.filter(
                        prefix=metadata_prefix
                    ).exists():
                        errors.append(
                            _error("cannotDisseminateFormat", metadata_prefix)
                        )
                    if "identifier" in params:
                        identifier = params.pop("identifier")[-1]
                        try:
                            header = Header.objects.get(identifier=identifier)
                        except Header.DoesNotExist:
                            errors.append(_error("idDoesNotExist", identifier))
                    else:
                        errors.append(_error("badArgument", "identifier"))
                else:
                    errors.append(
                        _error("badArgument_single", ";".join(metadata_prefix))
                    )
                    metadata_prefix = None
            else:
                errors.append(_error("badArgument", "metadataPrefix"))
            _check_bad_arguments(params, errors)
        elif verb == "Identify":
            template = "django_oai_pmh/identify.xml"
            _check_bad_arguments(params, errors)
        elif verb == "ListIdentifiers":
            template = "django_oai_pmh/listidentifiers.xml"

            if "resumptionToken" in params:
                header_list = Header.objects.all()
                (
                    paginator,
                    headers,
                    resumption_token,
                    set_spec,
                    metadata_prefix,
                    from_timestamp,
                    until_timestamp,
                ) = _do_resumption_token(params, errors, header_list)
            elif "metadataPrefix" in params:
                metadata_prefix = params.pop("metadataPrefix")
                if len(metadata_prefix) == 1:
                    metadata_prefix = metadata_prefix[0]
                    if not MetadataFormat.objects.filter(
                        prefix=metadata_prefix
                    ).exists():
                        errors.append(
                            _error("cannotDisseminateFormat", metadata_prefix)
                        )
                    else:
                        header_list = Header.objects.filter(
                            metadata_formats__prefix=metadata_prefix
                        )

                        if "set" in params:
                            if Set.objects.all().count() == 0:
                                errors.append(_error("noSetHierarchy"))
                            else:
                                set_spec = params.pop("set")[-1]
                                header_list = header_list.filter(sets__spec=set_spec)

                        from_timestamp, until_timestamp = _check_timestamps(
                            params, errors
                        )
                        if from_timestamp:
                            header_list = header_list.filter(
                                timestamp__gte=from_timestamp
                            )
                        if until_timestamp:
                            header_list = header_list.filter(
                                timestamp__lte=until_timestamp
                            )

                        if header_list.count() == 0 and not errors:
                            errors.append(_error("noRecordsMatch"))
                        else:
                            paginator = Paginator(header_list, NUM_PER_PAGE)
                            headers = paginator.page(1)
                else:
                    errors.append(
                        _error("badArgument_single", ";".join(metadata_prefix))
                    )
                    metadata_prefix = None
            else:
                errors.append(_error("badArgument", "metadataPrefix"))
            _check_bad_arguments(params, errors)
        elif verb == "ListMetadataFormats":
            template = "django_oai_pmh/listmetadataformats.xml"
            metadataformats = MetadataFormat.objects.all()

            if "identifier" in params:
                identifier = params.pop("identifier")[-1]
                if Header.objects.filter(identifier=identifier).exists():
                    metadataformats = metadataformats.filter(
                        identifiers__identifier=identifier
                    )
                else:
                    errors.append(_error("idDoesNotExist", identifier))
            if metadataformats.count() == 0:
                if identifier:
                    errors.append(_error("noMetadataFormats", identifier))
                else:
                    errors.append(_error("noMetadataFormats"))
            _check_bad_arguments(params, errors)
        elif verb == "ListRecords":
            template = "django_oai_pmh/listrecords.xml"

            if "resumptionToken" in params:
                header_list = Header.objects.all()
                (
                    paginator,
                    headers,
                    resumption_token,
                    set_spec,
                    metadata_prefix,
                    from_timestamp,
                    until_timestamp,
                ) = _do_resumption_token(params, errors, header_list)
            elif "metadataPrefix" in params:
                metadata_prefix = params.pop("metadataPrefix")
                if len(metadata_prefix) == 1:
                    metadata_prefix = metadata_prefix[0]
                    if not MetadataFormat.objects.filter(
                        prefix=metadata_prefix
                    ).exists():
                        errors.append(
                            _error("cannotDisseminateFormat", metadata_prefix)
                        )
                    else:
                        header_list = Header.objects.filter(
                            metadata_formats__prefix=metadata_prefix
                        )

                        if "set" in params:
                            if Set.objects.all().count() == 0:
                                errors.append(_error("noSetHierarchy"))
                            else:
                                set_spec = params.pop("set")[-1]
                                header_list = header_list.filter(sets__spec=set_spec)
                        from_timestamp, until_timestamp = _check_timestamps(
                            params, errors
                        )
                        if from_timestamp:
                            header_list = header_list.filter(
                                timestamp__gte=from_timestamp
                            )
                        if until_timestamp:
                            header_list = header_list.filter(
                                timestamp__lte=until_timestamp
                            )

                        if header_list.count() == 0 and not errors:
                            errors.append(_error("noRecordsMatch"))
                        else:
                            paginator = Paginator(header_list, NUM_PER_PAGE)
                            headers = paginator.page(1)
                else:
                    errors.append(
                        _error("badArgument_single", ";".join(metadata_prefix))
                    )
                    metadata_prefix = None
            else:
                errors.append(_error("badArgument", "metadataPrefix"))
        elif verb == "ListSets":
            template = "django_oai_pmh/listsets.xml"

            if not Set.objects.all().exists():
                errors.append(_error("noSetHierarchy"))
            else:
                (
                    paginator,
                    sets,
                    resumption_token,
                    set_spec,
                    metadata_prefix,
                    from_timestamp,
                    until_timestamp,
                ) = _do_resumption_token(params, errors, Set.objects.all())
            _check_bad_arguments(params, errors)
        else:
            errors.append(_error("badVerb", verb))
    else:
        errors.append(_error("badVerb"))

    return render(
        request,
        template if not errors else "django_oai_pmh/error.xml",
        locals(),
        content_type="text/xml",
    )


def _check_bad_arguments(params, errors, msg=None):
    for k, v in params.copy().items():
        errors.append(
            {
                "code": "badArgument",
                "msg": f'The argument "{k}" (value="{v}") included in the request is '
                + "not valid."
                + (f" {msg}" if msg else ""),
            }
        )
        params.pop(k)


def _check_timestamps(params, errors):
    from_timestamp = None
    until_timestamp = None

    granularity = None
    if "from" in params:
        f = params.pop("from")[-1]
        granularity = "%Y-%m-%dT%H:%M:%SZ %z" if "T" in f else "%Y-%m-%d %z"
        try:
            from_timestamp = datetime.strptime(f + " +0000", granularity)
        except Exception:
            errors.append(_error("badArgument_valid", f, "from"))

    if "until" in params:
        u = params.pop("until")[-1]
        ugranularity = "%Y-%m-%dT%H:%M:%SZ %z" if "T" in u else "%Y-%m-%d %z"
        if ugranularity == granularity or not granularity:
            try:
                until_timestamp = datetime.strptime(u + " +0000", granularity)
            except Exception:
                errors.append(_error("badArgument_valid", u, "until"))
        else:
            errors.append(_error("badArgument_granularity"))
    return from_timestamp, until_timestamp


def _do_resumption_token(params, errors, objs):
    set_spec = None
    metadata_prefix = None
    from_timestamp = None
    until_timestamp = None
    resumption_token = None
    if "resumptionToken" in params:
        resumption_token = params.pop("resumptionToken")[-1]
        try:
            rt = ResumptionToken.objects.get(token=resumption_token)
            if timezone.now() > rt.expiration_date:
                errors.append(_error("badResumptionToken_expired.", resumption_token))
            else:
                if rt.set_spec:
                    objs = objs.filter(sets=rt.set_spec)
                    set_spec = rt.set_spec.spec
                if rt.metadata_prefix:
                    objs = objs.filter(metadata_formats=rt.metadata_prefix)
                    metadata_prefix = rt.metadata_prefix.prefix
                if rt.from_timestamp:
                    objs = objs.filter(timestamp__gte=rt.from_timestamp)
                    from_timestamp = rt.from_timestamp
                if rt.until_timestamp:
                    objs = objs.filter(timestamp__gte=rt.until_timestamp)
                    until_timestamp = rt.until_timestamp

                paginator = Paginator(objs, NUM_PER_PAGE)
                try:
                    page = paginator.page(rt.cursor / NUM_PER_PAGE + 1)
                except EmptyPage:
                    errors.append(_error("badResumptionToken", resumption_token))
        except ResumptionToken.DoesNotExist:
            paginator = Paginator(objs, NUM_PER_PAGE)
            page = paginator.page(1)
            errors.append(_error("badResumptionToken", resumption_token))
        _check_bad_arguments(
            params,
            errors,
            msg="The usage of resumptionToken allows no other arguments.",
        )
    else:
        paginator = Paginator(objs, NUM_PER_PAGE)
        page = paginator.page(1)

    return (
        paginator,
        page,
        resumption_token,
        set_spec,
        metadata_prefix,
        from_timestamp,
        until_timestamp,
    )


def _error(code, *args):
    if code == "badArgument":
        return {
            "code": "badArgument",
            "msg": f'The required argument "{args[0]}" is missing in the request.',
        }
    elif code == "badArgument_granularity":
        return {
            "code": "badArgument",
            "msg": 'The granularity of the arguments "from" and "until" do not match.',
        }
    elif code == "badArgument_single":
        return {
            "code": "badArgument",
            "msg": "Only a single metadataPrefix argument is allowed, got "
            + f'"{args[0]}".',
        }
    elif code == "badArgument_valid":
        return {
            "code": "badArgument",
            "msg": f'The value "{args[0]}" of the argument "{args[1]}" is not valid.',
        }
    elif code == "badResumptionToken":
        return {
            "code": "badResumptionToken",
            "msg": f'The resumptionToken "{args[0]}" is invalid.',
        }
    elif code == "badResumptionToken_expired":
        return {
            "code": "badResumptionToken",
            "msg": f'The resumptionToken "{args[0]}" is expired.',
        }
    elif code == "badVerb" and len(args) == 0:
        return {"code": "badVerb", "msg": "The request does not provide any verb."}
    elif code == "badVerb":
        return {
            "code": "badVerb",
            "msg": f'The verb "{args[0]}" provided in the request is illegal.',
        }
    elif code == "cannotDisseminateFormat":
        return {
            "code": "cannotDisseminateFormat",
            "msg": f'The value of the metadataPrefix argument "{args[0]}" is not '
            + " supported.",
        }
    elif code == "idDoesNotExist":
        return {
            "code": "idDoesNotExist",
            "msg": f'A record with the identifier "{args[0]}" does not exist.',
        }
    elif code == "noMetadataFormats" and len(args) == 0:
        return {
            "code": "noMetadataFormats",
            "msg": "There are no metadata formats available.",
        }
    elif code == "noMetadataFormats":
        return {
            "code": "noMetadataFormats",
            "msg": "There are no metadata formats available for the record with "
            + f'identifier "{args[0]}".',
        }
    elif code == "noRecordsMatch":
        return {
            "code": "noRecordsMatch",
            "msg": "The combination of the values of the from, until, and set "
            + "arguments results in an empty list.",
        }
    elif code == "noSetHierarchy":
        return {
            "code": "noSetHierarchy",
            "msg": "This repository does not support sets.",
        }
