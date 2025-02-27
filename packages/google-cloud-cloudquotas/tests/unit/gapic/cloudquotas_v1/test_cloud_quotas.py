# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    import mock

from collections.abc import Iterable
import json
import math

from google.api_core import gapic_v1, grpc_helpers, grpc_helpers_async, path_template
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import json_format
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

from google.cloud.cloudquotas_v1.services.cloud_quotas import (
    CloudQuotasAsyncClient,
    CloudQuotasClient,
    pagers,
    transports,
)
from google.cloud.cloudquotas_v1.types import cloudquotas, resources


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert CloudQuotasClient._get_default_mtls_endpoint(None) is None
    assert (
        CloudQuotasClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        CloudQuotasClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        CloudQuotasClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        CloudQuotasClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert CloudQuotasClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (CloudQuotasClient, "grpc"),
        (CloudQuotasAsyncClient, "grpc_asyncio"),
        (CloudQuotasClient, "rest"),
    ],
)
def test_cloud_quotas_client_from_service_account_info(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "cloudquotas.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://cloudquotas.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.CloudQuotasGrpcTransport, "grpc"),
        (transports.CloudQuotasGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.CloudQuotasRestTransport, "rest"),
    ],
)
def test_cloud_quotas_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (CloudQuotasClient, "grpc"),
        (CloudQuotasAsyncClient, "grpc_asyncio"),
        (CloudQuotasClient, "rest"),
    ],
)
def test_cloud_quotas_client_from_service_account_file(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "cloudquotas.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://cloudquotas.googleapis.com"
        )


def test_cloud_quotas_client_get_transport_class():
    transport = CloudQuotasClient.get_transport_class()
    available_transports = [
        transports.CloudQuotasGrpcTransport,
        transports.CloudQuotasRestTransport,
    ]
    assert transport in available_transports

    transport = CloudQuotasClient.get_transport_class("grpc")
    assert transport == transports.CloudQuotasGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (CloudQuotasClient, transports.CloudQuotasGrpcTransport, "grpc"),
        (
            CloudQuotasAsyncClient,
            transports.CloudQuotasGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (CloudQuotasClient, transports.CloudQuotasRestTransport, "rest"),
    ],
)
@mock.patch.object(
    CloudQuotasClient, "DEFAULT_ENDPOINT", modify_default_endpoint(CloudQuotasClient)
)
@mock.patch.object(
    CloudQuotasAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CloudQuotasAsyncClient),
)
def test_cloud_quotas_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(CloudQuotasClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(CloudQuotasClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class(transport=transport_name)

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class(transport=transport_name)

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )
    # Check the case api_endpoint is provided
    options = client_options.ClientOptions(
        api_audience="https://language.googleapis.com"
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience="https://language.googleapis.com",
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (CloudQuotasClient, transports.CloudQuotasGrpcTransport, "grpc", "true"),
        (
            CloudQuotasAsyncClient,
            transports.CloudQuotasGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (CloudQuotasClient, transports.CloudQuotasGrpcTransport, "grpc", "false"),
        (
            CloudQuotasAsyncClient,
            transports.CloudQuotasGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (CloudQuotasClient, transports.CloudQuotasRestTransport, "rest", "true"),
        (CloudQuotasClient, transports.CloudQuotasRestTransport, "rest", "false"),
    ],
)
@mock.patch.object(
    CloudQuotasClient, "DEFAULT_ENDPOINT", modify_default_endpoint(CloudQuotasClient)
)
@mock.patch.object(
    CloudQuotasAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CloudQuotasAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_cloud_quotas_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client.DEFAULT_ENDPOINT
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client.DEFAULT_ENDPOINT
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                        api_audience=None,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize("client_class", [CloudQuotasClient, CloudQuotasAsyncClient])
@mock.patch.object(
    CloudQuotasClient, "DEFAULT_ENDPOINT", modify_default_endpoint(CloudQuotasClient)
)
@mock.patch.object(
    CloudQuotasAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CloudQuotasAsyncClient),
)
def test_cloud_quotas_client_get_mtls_endpoint_and_cert_source(client_class):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            with mock.patch(
                "google.auth.transport.mtls.default_client_cert_source",
                return_value=mock_client_cert_source,
            ):
                (
                    api_endpoint,
                    cert_source,
                ) = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (CloudQuotasClient, transports.CloudQuotasGrpcTransport, "grpc"),
        (
            CloudQuotasAsyncClient,
            transports.CloudQuotasGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (CloudQuotasClient, transports.CloudQuotasRestTransport, "rest"),
    ],
)
def test_cloud_quotas_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (CloudQuotasClient, transports.CloudQuotasGrpcTransport, "grpc", grpc_helpers),
        (
            CloudQuotasAsyncClient,
            transports.CloudQuotasGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (CloudQuotasClient, transports.CloudQuotasRestTransport, "rest", None),
    ],
)
def test_cloud_quotas_client_client_options_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


def test_cloud_quotas_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.cloudquotas_v1.services.cloud_quotas.transports.CloudQuotasGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = CloudQuotasClient(client_options={"api_endpoint": "squid.clam.whelk"})
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (CloudQuotasClient, transports.CloudQuotasGrpcTransport, "grpc", grpc_helpers),
        (
            CloudQuotasAsyncClient,
            transports.CloudQuotasGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_cloud_quotas_client_create_channel_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # test that the credentials from file are saved and used as the credentials.
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel"
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        file_creds = ga_credentials.AnonymousCredentials()
        load_creds.return_value = (file_creds, None)
        adc.return_value = (creds, None)
        client = client_class(client_options=options, transport=transport_name)
        create_channel.assert_called_with(
            "cloudquotas.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="cloudquotas.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudquotas.ListQuotaInfosRequest,
        dict,
    ],
)
def test_list_quota_infos(request_type, transport: str = "grpc"):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_quota_infos), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudquotas.ListQuotaInfosResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_quota_infos(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudquotas.ListQuotaInfosRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListQuotaInfosPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_quota_infos_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_quota_infos), "__call__") as call:
        client.list_quota_infos()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudquotas.ListQuotaInfosRequest()


@pytest.mark.asyncio
async def test_list_quota_infos_async(
    transport: str = "grpc_asyncio", request_type=cloudquotas.ListQuotaInfosRequest
):
    client = CloudQuotasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_quota_infos), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudquotas.ListQuotaInfosResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_quota_infos(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudquotas.ListQuotaInfosRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListQuotaInfosAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_quota_infos_async_from_dict():
    await test_list_quota_infos_async(request_type=dict)


def test_list_quota_infos_field_headers():
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudquotas.ListQuotaInfosRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_quota_infos), "__call__") as call:
        call.return_value = cloudquotas.ListQuotaInfosResponse()
        client.list_quota_infos(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_quota_infos_field_headers_async():
    client = CloudQuotasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudquotas.ListQuotaInfosRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_quota_infos), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudquotas.ListQuotaInfosResponse()
        )
        await client.list_quota_infos(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_quota_infos_flattened():
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_quota_infos), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudquotas.ListQuotaInfosResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_quota_infos(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_quota_infos_flattened_error():
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_quota_infos(
            cloudquotas.ListQuotaInfosRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_quota_infos_flattened_async():
    client = CloudQuotasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_quota_infos), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudquotas.ListQuotaInfosResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudquotas.ListQuotaInfosResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_quota_infos(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_quota_infos_flattened_error_async():
    client = CloudQuotasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_quota_infos(
            cloudquotas.ListQuotaInfosRequest(),
            parent="parent_value",
        )


def test_list_quota_infos_pager(transport_name: str = "grpc"):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_quota_infos), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudquotas.ListQuotaInfosResponse(
                quota_infos=[
                    resources.QuotaInfo(),
                    resources.QuotaInfo(),
                    resources.QuotaInfo(),
                ],
                next_page_token="abc",
            ),
            cloudquotas.ListQuotaInfosResponse(
                quota_infos=[],
                next_page_token="def",
            ),
            cloudquotas.ListQuotaInfosResponse(
                quota_infos=[
                    resources.QuotaInfo(),
                ],
                next_page_token="ghi",
            ),
            cloudquotas.ListQuotaInfosResponse(
                quota_infos=[
                    resources.QuotaInfo(),
                    resources.QuotaInfo(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_quota_infos(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.QuotaInfo) for i in results)


def test_list_quota_infos_pages(transport_name: str = "grpc"):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_quota_infos), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudquotas.ListQuotaInfosResponse(
                quota_infos=[
                    resources.QuotaInfo(),
                    resources.QuotaInfo(),
                    resources.QuotaInfo(),
                ],
                next_page_token="abc",
            ),
            cloudquotas.ListQuotaInfosResponse(
                quota_infos=[],
                next_page_token="def",
            ),
            cloudquotas.ListQuotaInfosResponse(
                quota_infos=[
                    resources.QuotaInfo(),
                ],
                next_page_token="ghi",
            ),
            cloudquotas.ListQuotaInfosResponse(
                quota_infos=[
                    resources.QuotaInfo(),
                    resources.QuotaInfo(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_quota_infos(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_quota_infos_async_pager():
    client = CloudQuotasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_quota_infos), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudquotas.ListQuotaInfosResponse(
                quota_infos=[
                    resources.QuotaInfo(),
                    resources.QuotaInfo(),
                    resources.QuotaInfo(),
                ],
                next_page_token="abc",
            ),
            cloudquotas.ListQuotaInfosResponse(
                quota_infos=[],
                next_page_token="def",
            ),
            cloudquotas.ListQuotaInfosResponse(
                quota_infos=[
                    resources.QuotaInfo(),
                ],
                next_page_token="ghi",
            ),
            cloudquotas.ListQuotaInfosResponse(
                quota_infos=[
                    resources.QuotaInfo(),
                    resources.QuotaInfo(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_quota_infos(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.QuotaInfo) for i in responses)


@pytest.mark.asyncio
async def test_list_quota_infos_async_pages():
    client = CloudQuotasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_quota_infos), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudquotas.ListQuotaInfosResponse(
                quota_infos=[
                    resources.QuotaInfo(),
                    resources.QuotaInfo(),
                    resources.QuotaInfo(),
                ],
                next_page_token="abc",
            ),
            cloudquotas.ListQuotaInfosResponse(
                quota_infos=[],
                next_page_token="def",
            ),
            cloudquotas.ListQuotaInfosResponse(
                quota_infos=[
                    resources.QuotaInfo(),
                ],
                next_page_token="ghi",
            ),
            cloudquotas.ListQuotaInfosResponse(
                quota_infos=[
                    resources.QuotaInfo(),
                    resources.QuotaInfo(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_quota_infos(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        cloudquotas.GetQuotaInfoRequest,
        dict,
    ],
)
def test_get_quota_info(request_type, transport: str = "grpc"):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_quota_info), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.QuotaInfo(
            name="name_value",
            quota_id="quota_id_value",
            metric="metric_value",
            service="service_value",
            is_precise=True,
            refresh_interval="refresh_interval_value",
            container_type=resources.QuotaInfo.ContainerType.PROJECT,
            dimensions=["dimensions_value"],
            metric_display_name="metric_display_name_value",
            quota_display_name="quota_display_name_value",
            metric_unit="metric_unit_value",
            is_fixed=True,
            is_concurrent=True,
            service_request_quota_uri="service_request_quota_uri_value",
        )
        response = client.get_quota_info(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudquotas.GetQuotaInfoRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.QuotaInfo)
    assert response.name == "name_value"
    assert response.quota_id == "quota_id_value"
    assert response.metric == "metric_value"
    assert response.service == "service_value"
    assert response.is_precise is True
    assert response.refresh_interval == "refresh_interval_value"
    assert response.container_type == resources.QuotaInfo.ContainerType.PROJECT
    assert response.dimensions == ["dimensions_value"]
    assert response.metric_display_name == "metric_display_name_value"
    assert response.quota_display_name == "quota_display_name_value"
    assert response.metric_unit == "metric_unit_value"
    assert response.is_fixed is True
    assert response.is_concurrent is True
    assert response.service_request_quota_uri == "service_request_quota_uri_value"


def test_get_quota_info_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_quota_info), "__call__") as call:
        client.get_quota_info()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudquotas.GetQuotaInfoRequest()


@pytest.mark.asyncio
async def test_get_quota_info_async(
    transport: str = "grpc_asyncio", request_type=cloudquotas.GetQuotaInfoRequest
):
    client = CloudQuotasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_quota_info), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.QuotaInfo(
                name="name_value",
                quota_id="quota_id_value",
                metric="metric_value",
                service="service_value",
                is_precise=True,
                refresh_interval="refresh_interval_value",
                container_type=resources.QuotaInfo.ContainerType.PROJECT,
                dimensions=["dimensions_value"],
                metric_display_name="metric_display_name_value",
                quota_display_name="quota_display_name_value",
                metric_unit="metric_unit_value",
                is_fixed=True,
                is_concurrent=True,
                service_request_quota_uri="service_request_quota_uri_value",
            )
        )
        response = await client.get_quota_info(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudquotas.GetQuotaInfoRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.QuotaInfo)
    assert response.name == "name_value"
    assert response.quota_id == "quota_id_value"
    assert response.metric == "metric_value"
    assert response.service == "service_value"
    assert response.is_precise is True
    assert response.refresh_interval == "refresh_interval_value"
    assert response.container_type == resources.QuotaInfo.ContainerType.PROJECT
    assert response.dimensions == ["dimensions_value"]
    assert response.metric_display_name == "metric_display_name_value"
    assert response.quota_display_name == "quota_display_name_value"
    assert response.metric_unit == "metric_unit_value"
    assert response.is_fixed is True
    assert response.is_concurrent is True
    assert response.service_request_quota_uri == "service_request_quota_uri_value"


@pytest.mark.asyncio
async def test_get_quota_info_async_from_dict():
    await test_get_quota_info_async(request_type=dict)


def test_get_quota_info_field_headers():
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudquotas.GetQuotaInfoRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_quota_info), "__call__") as call:
        call.return_value = resources.QuotaInfo()
        client.get_quota_info(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_quota_info_field_headers_async():
    client = CloudQuotasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudquotas.GetQuotaInfoRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_quota_info), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.QuotaInfo())
        await client.get_quota_info(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_quota_info_flattened():
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_quota_info), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.QuotaInfo()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_quota_info(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_quota_info_flattened_error():
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_quota_info(
            cloudquotas.GetQuotaInfoRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_quota_info_flattened_async():
    client = CloudQuotasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_quota_info), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.QuotaInfo()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.QuotaInfo())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_quota_info(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_quota_info_flattened_error_async():
    client = CloudQuotasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_quota_info(
            cloudquotas.GetQuotaInfoRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudquotas.ListQuotaPreferencesRequest,
        dict,
    ],
)
def test_list_quota_preferences(request_type, transport: str = "grpc"):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_quota_preferences), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudquotas.ListQuotaPreferencesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_quota_preferences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudquotas.ListQuotaPreferencesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListQuotaPreferencesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_quota_preferences_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_quota_preferences), "__call__"
    ) as call:
        client.list_quota_preferences()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudquotas.ListQuotaPreferencesRequest()


@pytest.mark.asyncio
async def test_list_quota_preferences_async(
    transport: str = "grpc_asyncio",
    request_type=cloudquotas.ListQuotaPreferencesRequest,
):
    client = CloudQuotasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_quota_preferences), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudquotas.ListQuotaPreferencesResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_quota_preferences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudquotas.ListQuotaPreferencesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListQuotaPreferencesAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_quota_preferences_async_from_dict():
    await test_list_quota_preferences_async(request_type=dict)


def test_list_quota_preferences_field_headers():
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudquotas.ListQuotaPreferencesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_quota_preferences), "__call__"
    ) as call:
        call.return_value = cloudquotas.ListQuotaPreferencesResponse()
        client.list_quota_preferences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_quota_preferences_field_headers_async():
    client = CloudQuotasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudquotas.ListQuotaPreferencesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_quota_preferences), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudquotas.ListQuotaPreferencesResponse()
        )
        await client.list_quota_preferences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_quota_preferences_flattened():
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_quota_preferences), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudquotas.ListQuotaPreferencesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_quota_preferences(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_quota_preferences_flattened_error():
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_quota_preferences(
            cloudquotas.ListQuotaPreferencesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_quota_preferences_flattened_async():
    client = CloudQuotasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_quota_preferences), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudquotas.ListQuotaPreferencesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudquotas.ListQuotaPreferencesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_quota_preferences(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_quota_preferences_flattened_error_async():
    client = CloudQuotasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_quota_preferences(
            cloudquotas.ListQuotaPreferencesRequest(),
            parent="parent_value",
        )


def test_list_quota_preferences_pager(transport_name: str = "grpc"):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_quota_preferences), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudquotas.ListQuotaPreferencesResponse(
                quota_preferences=[
                    resources.QuotaPreference(),
                    resources.QuotaPreference(),
                    resources.QuotaPreference(),
                ],
                next_page_token="abc",
            ),
            cloudquotas.ListQuotaPreferencesResponse(
                quota_preferences=[],
                next_page_token="def",
            ),
            cloudquotas.ListQuotaPreferencesResponse(
                quota_preferences=[
                    resources.QuotaPreference(),
                ],
                next_page_token="ghi",
            ),
            cloudquotas.ListQuotaPreferencesResponse(
                quota_preferences=[
                    resources.QuotaPreference(),
                    resources.QuotaPreference(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_quota_preferences(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.QuotaPreference) for i in results)


def test_list_quota_preferences_pages(transport_name: str = "grpc"):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_quota_preferences), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudquotas.ListQuotaPreferencesResponse(
                quota_preferences=[
                    resources.QuotaPreference(),
                    resources.QuotaPreference(),
                    resources.QuotaPreference(),
                ],
                next_page_token="abc",
            ),
            cloudquotas.ListQuotaPreferencesResponse(
                quota_preferences=[],
                next_page_token="def",
            ),
            cloudquotas.ListQuotaPreferencesResponse(
                quota_preferences=[
                    resources.QuotaPreference(),
                ],
                next_page_token="ghi",
            ),
            cloudquotas.ListQuotaPreferencesResponse(
                quota_preferences=[
                    resources.QuotaPreference(),
                    resources.QuotaPreference(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_quota_preferences(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_quota_preferences_async_pager():
    client = CloudQuotasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_quota_preferences),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudquotas.ListQuotaPreferencesResponse(
                quota_preferences=[
                    resources.QuotaPreference(),
                    resources.QuotaPreference(),
                    resources.QuotaPreference(),
                ],
                next_page_token="abc",
            ),
            cloudquotas.ListQuotaPreferencesResponse(
                quota_preferences=[],
                next_page_token="def",
            ),
            cloudquotas.ListQuotaPreferencesResponse(
                quota_preferences=[
                    resources.QuotaPreference(),
                ],
                next_page_token="ghi",
            ),
            cloudquotas.ListQuotaPreferencesResponse(
                quota_preferences=[
                    resources.QuotaPreference(),
                    resources.QuotaPreference(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_quota_preferences(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.QuotaPreference) for i in responses)


@pytest.mark.asyncio
async def test_list_quota_preferences_async_pages():
    client = CloudQuotasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_quota_preferences),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudquotas.ListQuotaPreferencesResponse(
                quota_preferences=[
                    resources.QuotaPreference(),
                    resources.QuotaPreference(),
                    resources.QuotaPreference(),
                ],
                next_page_token="abc",
            ),
            cloudquotas.ListQuotaPreferencesResponse(
                quota_preferences=[],
                next_page_token="def",
            ),
            cloudquotas.ListQuotaPreferencesResponse(
                quota_preferences=[
                    resources.QuotaPreference(),
                ],
                next_page_token="ghi",
            ),
            cloudquotas.ListQuotaPreferencesResponse(
                quota_preferences=[
                    resources.QuotaPreference(),
                    resources.QuotaPreference(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_quota_preferences(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        cloudquotas.GetQuotaPreferenceRequest,
        dict,
    ],
)
def test_get_quota_preference(request_type, transport: str = "grpc"):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_quota_preference), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.QuotaPreference(
            name="name_value",
            etag="etag_value",
            service="service_value",
            quota_id="quota_id_value",
            reconciling=True,
            justification="justification_value",
            contact_email="contact_email_value",
        )
        response = client.get_quota_preference(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudquotas.GetQuotaPreferenceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.QuotaPreference)
    assert response.name == "name_value"
    assert response.etag == "etag_value"
    assert response.service == "service_value"
    assert response.quota_id == "quota_id_value"
    assert response.reconciling is True
    assert response.justification == "justification_value"
    assert response.contact_email == "contact_email_value"


def test_get_quota_preference_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_quota_preference), "__call__"
    ) as call:
        client.get_quota_preference()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudquotas.GetQuotaPreferenceRequest()


@pytest.mark.asyncio
async def test_get_quota_preference_async(
    transport: str = "grpc_asyncio", request_type=cloudquotas.GetQuotaPreferenceRequest
):
    client = CloudQuotasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_quota_preference), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.QuotaPreference(
                name="name_value",
                etag="etag_value",
                service="service_value",
                quota_id="quota_id_value",
                reconciling=True,
                justification="justification_value",
                contact_email="contact_email_value",
            )
        )
        response = await client.get_quota_preference(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudquotas.GetQuotaPreferenceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.QuotaPreference)
    assert response.name == "name_value"
    assert response.etag == "etag_value"
    assert response.service == "service_value"
    assert response.quota_id == "quota_id_value"
    assert response.reconciling is True
    assert response.justification == "justification_value"
    assert response.contact_email == "contact_email_value"


@pytest.mark.asyncio
async def test_get_quota_preference_async_from_dict():
    await test_get_quota_preference_async(request_type=dict)


def test_get_quota_preference_field_headers():
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudquotas.GetQuotaPreferenceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_quota_preference), "__call__"
    ) as call:
        call.return_value = resources.QuotaPreference()
        client.get_quota_preference(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_quota_preference_field_headers_async():
    client = CloudQuotasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudquotas.GetQuotaPreferenceRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_quota_preference), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.QuotaPreference()
        )
        await client.get_quota_preference(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_quota_preference_flattened():
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_quota_preference), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.QuotaPreference()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_quota_preference(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_quota_preference_flattened_error():
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_quota_preference(
            cloudquotas.GetQuotaPreferenceRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_quota_preference_flattened_async():
    client = CloudQuotasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_quota_preference), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.QuotaPreference()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.QuotaPreference()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_quota_preference(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_quota_preference_flattened_error_async():
    client = CloudQuotasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_quota_preference(
            cloudquotas.GetQuotaPreferenceRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudquotas.CreateQuotaPreferenceRequest,
        dict,
    ],
)
def test_create_quota_preference(request_type, transport: str = "grpc"):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_quota_preference), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.QuotaPreference(
            name="name_value",
            etag="etag_value",
            service="service_value",
            quota_id="quota_id_value",
            reconciling=True,
            justification="justification_value",
            contact_email="contact_email_value",
        )
        response = client.create_quota_preference(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudquotas.CreateQuotaPreferenceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.QuotaPreference)
    assert response.name == "name_value"
    assert response.etag == "etag_value"
    assert response.service == "service_value"
    assert response.quota_id == "quota_id_value"
    assert response.reconciling is True
    assert response.justification == "justification_value"
    assert response.contact_email == "contact_email_value"


def test_create_quota_preference_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_quota_preference), "__call__"
    ) as call:
        client.create_quota_preference()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudquotas.CreateQuotaPreferenceRequest()


@pytest.mark.asyncio
async def test_create_quota_preference_async(
    transport: str = "grpc_asyncio",
    request_type=cloudquotas.CreateQuotaPreferenceRequest,
):
    client = CloudQuotasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_quota_preference), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.QuotaPreference(
                name="name_value",
                etag="etag_value",
                service="service_value",
                quota_id="quota_id_value",
                reconciling=True,
                justification="justification_value",
                contact_email="contact_email_value",
            )
        )
        response = await client.create_quota_preference(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudquotas.CreateQuotaPreferenceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.QuotaPreference)
    assert response.name == "name_value"
    assert response.etag == "etag_value"
    assert response.service == "service_value"
    assert response.quota_id == "quota_id_value"
    assert response.reconciling is True
    assert response.justification == "justification_value"
    assert response.contact_email == "contact_email_value"


@pytest.mark.asyncio
async def test_create_quota_preference_async_from_dict():
    await test_create_quota_preference_async(request_type=dict)


def test_create_quota_preference_field_headers():
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudquotas.CreateQuotaPreferenceRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_quota_preference), "__call__"
    ) as call:
        call.return_value = resources.QuotaPreference()
        client.create_quota_preference(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_quota_preference_field_headers_async():
    client = CloudQuotasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudquotas.CreateQuotaPreferenceRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_quota_preference), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.QuotaPreference()
        )
        await client.create_quota_preference(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_quota_preference_flattened():
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_quota_preference), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.QuotaPreference()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_quota_preference(
            parent="parent_value",
            quota_preference=resources.QuotaPreference(name="name_value"),
            quota_preference_id="quota_preference_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].quota_preference
        mock_val = resources.QuotaPreference(name="name_value")
        assert arg == mock_val
        arg = args[0].quota_preference_id
        mock_val = "quota_preference_id_value"
        assert arg == mock_val


def test_create_quota_preference_flattened_error():
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_quota_preference(
            cloudquotas.CreateQuotaPreferenceRequest(),
            parent="parent_value",
            quota_preference=resources.QuotaPreference(name="name_value"),
            quota_preference_id="quota_preference_id_value",
        )


@pytest.mark.asyncio
async def test_create_quota_preference_flattened_async():
    client = CloudQuotasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_quota_preference), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.QuotaPreference()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.QuotaPreference()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_quota_preference(
            parent="parent_value",
            quota_preference=resources.QuotaPreference(name="name_value"),
            quota_preference_id="quota_preference_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].quota_preference
        mock_val = resources.QuotaPreference(name="name_value")
        assert arg == mock_val
        arg = args[0].quota_preference_id
        mock_val = "quota_preference_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_quota_preference_flattened_error_async():
    client = CloudQuotasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_quota_preference(
            cloudquotas.CreateQuotaPreferenceRequest(),
            parent="parent_value",
            quota_preference=resources.QuotaPreference(name="name_value"),
            quota_preference_id="quota_preference_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudquotas.UpdateQuotaPreferenceRequest,
        dict,
    ],
)
def test_update_quota_preference(request_type, transport: str = "grpc"):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_quota_preference), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.QuotaPreference(
            name="name_value",
            etag="etag_value",
            service="service_value",
            quota_id="quota_id_value",
            reconciling=True,
            justification="justification_value",
            contact_email="contact_email_value",
        )
        response = client.update_quota_preference(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudquotas.UpdateQuotaPreferenceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.QuotaPreference)
    assert response.name == "name_value"
    assert response.etag == "etag_value"
    assert response.service == "service_value"
    assert response.quota_id == "quota_id_value"
    assert response.reconciling is True
    assert response.justification == "justification_value"
    assert response.contact_email == "contact_email_value"


def test_update_quota_preference_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_quota_preference), "__call__"
    ) as call:
        client.update_quota_preference()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudquotas.UpdateQuotaPreferenceRequest()


@pytest.mark.asyncio
async def test_update_quota_preference_async(
    transport: str = "grpc_asyncio",
    request_type=cloudquotas.UpdateQuotaPreferenceRequest,
):
    client = CloudQuotasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_quota_preference), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.QuotaPreference(
                name="name_value",
                etag="etag_value",
                service="service_value",
                quota_id="quota_id_value",
                reconciling=True,
                justification="justification_value",
                contact_email="contact_email_value",
            )
        )
        response = await client.update_quota_preference(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloudquotas.UpdateQuotaPreferenceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.QuotaPreference)
    assert response.name == "name_value"
    assert response.etag == "etag_value"
    assert response.service == "service_value"
    assert response.quota_id == "quota_id_value"
    assert response.reconciling is True
    assert response.justification == "justification_value"
    assert response.contact_email == "contact_email_value"


@pytest.mark.asyncio
async def test_update_quota_preference_async_from_dict():
    await test_update_quota_preference_async(request_type=dict)


def test_update_quota_preference_field_headers():
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudquotas.UpdateQuotaPreferenceRequest()

    request.quota_preference.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_quota_preference), "__call__"
    ) as call:
        call.return_value = resources.QuotaPreference()
        client.update_quota_preference(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "quota_preference.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_quota_preference_field_headers_async():
    client = CloudQuotasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudquotas.UpdateQuotaPreferenceRequest()

    request.quota_preference.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_quota_preference), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.QuotaPreference()
        )
        await client.update_quota_preference(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "quota_preference.name=name_value",
    ) in kw["metadata"]


def test_update_quota_preference_flattened():
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_quota_preference), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.QuotaPreference()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_quota_preference(
            quota_preference=resources.QuotaPreference(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].quota_preference
        mock_val = resources.QuotaPreference(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_quota_preference_flattened_error():
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_quota_preference(
            cloudquotas.UpdateQuotaPreferenceRequest(),
            quota_preference=resources.QuotaPreference(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_quota_preference_flattened_async():
    client = CloudQuotasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_quota_preference), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.QuotaPreference()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.QuotaPreference()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_quota_preference(
            quota_preference=resources.QuotaPreference(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].quota_preference
        mock_val = resources.QuotaPreference(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_quota_preference_flattened_error_async():
    client = CloudQuotasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_quota_preference(
            cloudquotas.UpdateQuotaPreferenceRequest(),
            quota_preference=resources.QuotaPreference(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudquotas.ListQuotaInfosRequest,
        dict,
    ],
)
def test_list_quota_infos_rest(request_type):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/services/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloudquotas.ListQuotaInfosResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = cloudquotas.ListQuotaInfosResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_quota_infos(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListQuotaInfosPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_quota_infos_rest_required_fields(
    request_type=cloudquotas.ListQuotaInfosRequest,
):
    transport_class = transports.CloudQuotasRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_quota_infos._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_quota_infos._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = cloudquotas.ListQuotaInfosResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = cloudquotas.ListQuotaInfosResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_quota_infos(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_quota_infos_rest_unset_required_fields():
    transport = transports.CloudQuotasRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_quota_infos._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_quota_infos_rest_interceptors(null_interceptor):
    transport = transports.CloudQuotasRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudQuotasRestInterceptor(),
    )
    client = CloudQuotasClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CloudQuotasRestInterceptor, "post_list_quota_infos"
    ) as post, mock.patch.object(
        transports.CloudQuotasRestInterceptor, "pre_list_quota_infos"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloudquotas.ListQuotaInfosRequest.pb(
            cloudquotas.ListQuotaInfosRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = cloudquotas.ListQuotaInfosResponse.to_json(
            cloudquotas.ListQuotaInfosResponse()
        )

        request = cloudquotas.ListQuotaInfosRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = cloudquotas.ListQuotaInfosResponse()

        client.list_quota_infos(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_quota_infos_rest_bad_request(
    transport: str = "rest", request_type=cloudquotas.ListQuotaInfosRequest
):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/services/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_quota_infos(request)


def test_list_quota_infos_rest_flattened():
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloudquotas.ListQuotaInfosResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/services/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = cloudquotas.ListQuotaInfosResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_quota_infos(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/services/*}/quotaInfos"
            % client.transport._host,
            args[1],
        )


def test_list_quota_infos_rest_flattened_error(transport: str = "rest"):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_quota_infos(
            cloudquotas.ListQuotaInfosRequest(),
            parent="parent_value",
        )


def test_list_quota_infos_rest_pager(transport: str = "rest"):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            cloudquotas.ListQuotaInfosResponse(
                quota_infos=[
                    resources.QuotaInfo(),
                    resources.QuotaInfo(),
                    resources.QuotaInfo(),
                ],
                next_page_token="abc",
            ),
            cloudquotas.ListQuotaInfosResponse(
                quota_infos=[],
                next_page_token="def",
            ),
            cloudquotas.ListQuotaInfosResponse(
                quota_infos=[
                    resources.QuotaInfo(),
                ],
                next_page_token="ghi",
            ),
            cloudquotas.ListQuotaInfosResponse(
                quota_infos=[
                    resources.QuotaInfo(),
                    resources.QuotaInfo(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            cloudquotas.ListQuotaInfosResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/services/sample3"
        }

        pager = client.list_quota_infos(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.QuotaInfo) for i in results)

        pages = list(client.list_quota_infos(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        cloudquotas.GetQuotaInfoRequest,
        dict,
    ],
)
def test_get_quota_info_rest(request_type):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/services/sample3/quotaInfos/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.QuotaInfo(
            name="name_value",
            quota_id="quota_id_value",
            metric="metric_value",
            service="service_value",
            is_precise=True,
            refresh_interval="refresh_interval_value",
            container_type=resources.QuotaInfo.ContainerType.PROJECT,
            dimensions=["dimensions_value"],
            metric_display_name="metric_display_name_value",
            quota_display_name="quota_display_name_value",
            metric_unit="metric_unit_value",
            is_fixed=True,
            is_concurrent=True,
            service_request_quota_uri="service_request_quota_uri_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.QuotaInfo.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_quota_info(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.QuotaInfo)
    assert response.name == "name_value"
    assert response.quota_id == "quota_id_value"
    assert response.metric == "metric_value"
    assert response.service == "service_value"
    assert response.is_precise is True
    assert response.refresh_interval == "refresh_interval_value"
    assert response.container_type == resources.QuotaInfo.ContainerType.PROJECT
    assert response.dimensions == ["dimensions_value"]
    assert response.metric_display_name == "metric_display_name_value"
    assert response.quota_display_name == "quota_display_name_value"
    assert response.metric_unit == "metric_unit_value"
    assert response.is_fixed is True
    assert response.is_concurrent is True
    assert response.service_request_quota_uri == "service_request_quota_uri_value"


def test_get_quota_info_rest_required_fields(
    request_type=cloudquotas.GetQuotaInfoRequest,
):
    transport_class = transports.CloudQuotasRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_quota_info._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_quota_info._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.QuotaInfo()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = resources.QuotaInfo.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_quota_info(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_quota_info_rest_unset_required_fields():
    transport = transports.CloudQuotasRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_quota_info._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_quota_info_rest_interceptors(null_interceptor):
    transport = transports.CloudQuotasRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudQuotasRestInterceptor(),
    )
    client = CloudQuotasClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CloudQuotasRestInterceptor, "post_get_quota_info"
    ) as post, mock.patch.object(
        transports.CloudQuotasRestInterceptor, "pre_get_quota_info"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloudquotas.GetQuotaInfoRequest.pb(
            cloudquotas.GetQuotaInfoRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = resources.QuotaInfo.to_json(resources.QuotaInfo())

        request = cloudquotas.GetQuotaInfoRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.QuotaInfo()

        client.get_quota_info(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_quota_info_rest_bad_request(
    transport: str = "rest", request_type=cloudquotas.GetQuotaInfoRequest
):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/services/sample3/quotaInfos/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_quota_info(request)


def test_get_quota_info_rest_flattened():
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.QuotaInfo()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/services/sample3/quotaInfos/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.QuotaInfo.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_quota_info(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/services/*/quotaInfos/*}"
            % client.transport._host,
            args[1],
        )


def test_get_quota_info_rest_flattened_error(transport: str = "rest"):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_quota_info(
            cloudquotas.GetQuotaInfoRequest(),
            name="name_value",
        )


def test_get_quota_info_rest_error():
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudquotas.ListQuotaPreferencesRequest,
        dict,
    ],
)
def test_list_quota_preferences_rest(request_type):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloudquotas.ListQuotaPreferencesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = cloudquotas.ListQuotaPreferencesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_quota_preferences(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListQuotaPreferencesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_quota_preferences_rest_required_fields(
    request_type=cloudquotas.ListQuotaPreferencesRequest,
):
    transport_class = transports.CloudQuotasRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_quota_preferences._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_quota_preferences._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "order_by",
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = cloudquotas.ListQuotaPreferencesResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = cloudquotas.ListQuotaPreferencesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_quota_preferences(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_quota_preferences_rest_unset_required_fields():
    transport = transports.CloudQuotasRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_quota_preferences._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "orderBy",
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_quota_preferences_rest_interceptors(null_interceptor):
    transport = transports.CloudQuotasRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudQuotasRestInterceptor(),
    )
    client = CloudQuotasClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CloudQuotasRestInterceptor, "post_list_quota_preferences"
    ) as post, mock.patch.object(
        transports.CloudQuotasRestInterceptor, "pre_list_quota_preferences"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloudquotas.ListQuotaPreferencesRequest.pb(
            cloudquotas.ListQuotaPreferencesRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = cloudquotas.ListQuotaPreferencesResponse.to_json(
            cloudquotas.ListQuotaPreferencesResponse()
        )

        request = cloudquotas.ListQuotaPreferencesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = cloudquotas.ListQuotaPreferencesResponse()

        client.list_quota_preferences(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_quota_preferences_rest_bad_request(
    transport: str = "rest", request_type=cloudquotas.ListQuotaPreferencesRequest
):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_quota_preferences(request)


def test_list_quota_preferences_rest_flattened():
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = cloudquotas.ListQuotaPreferencesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = cloudquotas.ListQuotaPreferencesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_quota_preferences(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/quotaPreferences"
            % client.transport._host,
            args[1],
        )


def test_list_quota_preferences_rest_flattened_error(transport: str = "rest"):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_quota_preferences(
            cloudquotas.ListQuotaPreferencesRequest(),
            parent="parent_value",
        )


def test_list_quota_preferences_rest_pager(transport: str = "rest"):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            cloudquotas.ListQuotaPreferencesResponse(
                quota_preferences=[
                    resources.QuotaPreference(),
                    resources.QuotaPreference(),
                    resources.QuotaPreference(),
                ],
                next_page_token="abc",
            ),
            cloudquotas.ListQuotaPreferencesResponse(
                quota_preferences=[],
                next_page_token="def",
            ),
            cloudquotas.ListQuotaPreferencesResponse(
                quota_preferences=[
                    resources.QuotaPreference(),
                ],
                next_page_token="ghi",
            ),
            cloudquotas.ListQuotaPreferencesResponse(
                quota_preferences=[
                    resources.QuotaPreference(),
                    resources.QuotaPreference(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            cloudquotas.ListQuotaPreferencesResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_quota_preferences(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.QuotaPreference) for i in results)

        pages = list(client.list_quota_preferences(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        cloudquotas.GetQuotaPreferenceRequest,
        dict,
    ],
)
def test_get_quota_preference_rest(request_type):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/quotaPreferences/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.QuotaPreference(
            name="name_value",
            etag="etag_value",
            service="service_value",
            quota_id="quota_id_value",
            reconciling=True,
            justification="justification_value",
            contact_email="contact_email_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.QuotaPreference.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_quota_preference(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.QuotaPreference)
    assert response.name == "name_value"
    assert response.etag == "etag_value"
    assert response.service == "service_value"
    assert response.quota_id == "quota_id_value"
    assert response.reconciling is True
    assert response.justification == "justification_value"
    assert response.contact_email == "contact_email_value"


def test_get_quota_preference_rest_required_fields(
    request_type=cloudquotas.GetQuotaPreferenceRequest,
):
    transport_class = transports.CloudQuotasRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_quota_preference._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_quota_preference._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.QuotaPreference()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = resources.QuotaPreference.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_quota_preference(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_quota_preference_rest_unset_required_fields():
    transport = transports.CloudQuotasRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_quota_preference._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_quota_preference_rest_interceptors(null_interceptor):
    transport = transports.CloudQuotasRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudQuotasRestInterceptor(),
    )
    client = CloudQuotasClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CloudQuotasRestInterceptor, "post_get_quota_preference"
    ) as post, mock.patch.object(
        transports.CloudQuotasRestInterceptor, "pre_get_quota_preference"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloudquotas.GetQuotaPreferenceRequest.pb(
            cloudquotas.GetQuotaPreferenceRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = resources.QuotaPreference.to_json(
            resources.QuotaPreference()
        )

        request = cloudquotas.GetQuotaPreferenceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.QuotaPreference()

        client.get_quota_preference(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_quota_preference_rest_bad_request(
    transport: str = "rest", request_type=cloudquotas.GetQuotaPreferenceRequest
):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/quotaPreferences/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_quota_preference(request)


def test_get_quota_preference_rest_flattened():
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.QuotaPreference()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/quotaPreferences/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.QuotaPreference.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_quota_preference(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/quotaPreferences/*}"
            % client.transport._host,
            args[1],
        )


def test_get_quota_preference_rest_flattened_error(transport: str = "rest"):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_quota_preference(
            cloudquotas.GetQuotaPreferenceRequest(),
            name="name_value",
        )


def test_get_quota_preference_rest_error():
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudquotas.CreateQuotaPreferenceRequest,
        dict,
    ],
)
def test_create_quota_preference_rest(request_type):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["quota_preference"] = {
        "name": "name_value",
        "dimensions": {},
        "quota_config": {
            "preferred_value": 1595,
            "state_detail": "state_detail_value",
            "granted_value": {"value": 541},
            "trace_id": "trace_id_value",
            "annotations": {},
            "request_origin": 1,
        },
        "etag": "etag_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "service": "service_value",
        "quota_id": "quota_id_value",
        "reconciling": True,
        "justification": "justification_value",
        "contact_email": "contact_email_value",
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = cloudquotas.CreateQuotaPreferenceRequest.meta.fields[
        "quota_preference"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["quota_preference"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["quota_preference"][field])):
                    del request_init["quota_preference"][field][i][subfield]
            else:
                del request_init["quota_preference"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.QuotaPreference(
            name="name_value",
            etag="etag_value",
            service="service_value",
            quota_id="quota_id_value",
            reconciling=True,
            justification="justification_value",
            contact_email="contact_email_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.QuotaPreference.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_quota_preference(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.QuotaPreference)
    assert response.name == "name_value"
    assert response.etag == "etag_value"
    assert response.service == "service_value"
    assert response.quota_id == "quota_id_value"
    assert response.reconciling is True
    assert response.justification == "justification_value"
    assert response.contact_email == "contact_email_value"


def test_create_quota_preference_rest_required_fields(
    request_type=cloudquotas.CreateQuotaPreferenceRequest,
):
    transport_class = transports.CloudQuotasRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_quota_preference._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_quota_preference._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "ignore_safety_checks",
            "quota_preference_id",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.QuotaPreference()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = resources.QuotaPreference.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_quota_preference(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_quota_preference_rest_unset_required_fields():
    transport = transports.CloudQuotasRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_quota_preference._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "ignoreSafetyChecks",
                "quotaPreferenceId",
            )
        )
        & set(
            (
                "parent",
                "quotaPreference",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_quota_preference_rest_interceptors(null_interceptor):
    transport = transports.CloudQuotasRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudQuotasRestInterceptor(),
    )
    client = CloudQuotasClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CloudQuotasRestInterceptor, "post_create_quota_preference"
    ) as post, mock.patch.object(
        transports.CloudQuotasRestInterceptor, "pre_create_quota_preference"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloudquotas.CreateQuotaPreferenceRequest.pb(
            cloudquotas.CreateQuotaPreferenceRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = resources.QuotaPreference.to_json(
            resources.QuotaPreference()
        )

        request = cloudquotas.CreateQuotaPreferenceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.QuotaPreference()

        client.create_quota_preference(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_quota_preference_rest_bad_request(
    transport: str = "rest", request_type=cloudquotas.CreateQuotaPreferenceRequest
):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_quota_preference(request)


def test_create_quota_preference_rest_flattened():
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.QuotaPreference()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            quota_preference=resources.QuotaPreference(name="name_value"),
            quota_preference_id="quota_preference_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.QuotaPreference.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_quota_preference(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/quotaPreferences"
            % client.transport._host,
            args[1],
        )


def test_create_quota_preference_rest_flattened_error(transport: str = "rest"):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_quota_preference(
            cloudquotas.CreateQuotaPreferenceRequest(),
            parent="parent_value",
            quota_preference=resources.QuotaPreference(name="name_value"),
            quota_preference_id="quota_preference_id_value",
        )


def test_create_quota_preference_rest_error():
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        cloudquotas.UpdateQuotaPreferenceRequest,
        dict,
    ],
)
def test_update_quota_preference_rest(request_type):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "quota_preference": {
            "name": "projects/sample1/locations/sample2/quotaPreferences/sample3"
        }
    }
    request_init["quota_preference"] = {
        "name": "projects/sample1/locations/sample2/quotaPreferences/sample3",
        "dimensions": {},
        "quota_config": {
            "preferred_value": 1595,
            "state_detail": "state_detail_value",
            "granted_value": {"value": 541},
            "trace_id": "trace_id_value",
            "annotations": {},
            "request_origin": 1,
        },
        "etag": "etag_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "service": "service_value",
        "quota_id": "quota_id_value",
        "reconciling": True,
        "justification": "justification_value",
        "contact_email": "contact_email_value",
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = cloudquotas.UpdateQuotaPreferenceRequest.meta.fields[
        "quota_preference"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["quota_preference"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["quota_preference"][field])):
                    del request_init["quota_preference"][field][i][subfield]
            else:
                del request_init["quota_preference"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.QuotaPreference(
            name="name_value",
            etag="etag_value",
            service="service_value",
            quota_id="quota_id_value",
            reconciling=True,
            justification="justification_value",
            contact_email="contact_email_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.QuotaPreference.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_quota_preference(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.QuotaPreference)
    assert response.name == "name_value"
    assert response.etag == "etag_value"
    assert response.service == "service_value"
    assert response.quota_id == "quota_id_value"
    assert response.reconciling is True
    assert response.justification == "justification_value"
    assert response.contact_email == "contact_email_value"


def test_update_quota_preference_rest_required_fields(
    request_type=cloudquotas.UpdateQuotaPreferenceRequest,
):
    transport_class = transports.CloudQuotasRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(
            pb_request,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_quota_preference._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_quota_preference._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "allow_missing",
            "ignore_safety_checks",
            "update_mask",
            "validate_only",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.QuotaPreference()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = resources.QuotaPreference.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_quota_preference(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_quota_preference_rest_unset_required_fields():
    transport = transports.CloudQuotasRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_quota_preference._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "allowMissing",
                "ignoreSafetyChecks",
                "updateMask",
                "validateOnly",
            )
        )
        & set(("quotaPreference",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_quota_preference_rest_interceptors(null_interceptor):
    transport = transports.CloudQuotasRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.CloudQuotasRestInterceptor(),
    )
    client = CloudQuotasClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.CloudQuotasRestInterceptor, "post_update_quota_preference"
    ) as post, mock.patch.object(
        transports.CloudQuotasRestInterceptor, "pre_update_quota_preference"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = cloudquotas.UpdateQuotaPreferenceRequest.pb(
            cloudquotas.UpdateQuotaPreferenceRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = resources.QuotaPreference.to_json(
            resources.QuotaPreference()
        )

        request = cloudquotas.UpdateQuotaPreferenceRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.QuotaPreference()

        client.update_quota_preference(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_quota_preference_rest_bad_request(
    transport: str = "rest", request_type=cloudquotas.UpdateQuotaPreferenceRequest
):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "quota_preference": {
            "name": "projects/sample1/locations/sample2/quotaPreferences/sample3"
        }
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_quota_preference(request)


def test_update_quota_preference_rest_flattened():
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.QuotaPreference()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "quota_preference": {
                "name": "projects/sample1/locations/sample2/quotaPreferences/sample3"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            quota_preference=resources.QuotaPreference(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.QuotaPreference.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_quota_preference(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{quota_preference.name=projects/*/locations/*/quotaPreferences/*}"
            % client.transport._host,
            args[1],
        )


def test_update_quota_preference_rest_flattened_error(transport: str = "rest"):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_quota_preference(
            cloudquotas.UpdateQuotaPreferenceRequest(),
            quota_preference=resources.QuotaPreference(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_quota_preference_rest_error():
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.CloudQuotasGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudQuotasClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.CloudQuotasGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudQuotasClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.CloudQuotasGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = CloudQuotasClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = CloudQuotasClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.CloudQuotasGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudQuotasClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CloudQuotasGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = CloudQuotasClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CloudQuotasGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.CloudQuotasGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CloudQuotasGrpcTransport,
        transports.CloudQuotasGrpcAsyncIOTransport,
        transports.CloudQuotasRestTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "rest",
    ],
)
def test_transport_kind(transport_name):
    transport = CloudQuotasClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.CloudQuotasGrpcTransport,
    )


def test_cloud_quotas_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.CloudQuotasTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_cloud_quotas_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.cloudquotas_v1.services.cloud_quotas.transports.CloudQuotasTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.CloudQuotasTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_quota_infos",
        "get_quota_info",
        "list_quota_preferences",
        "get_quota_preference",
        "create_quota_preference",
        "update_quota_preference",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Catch all for all remaining methods and properties
    remainder = [
        "kind",
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_cloud_quotas_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.cloudquotas_v1.services.cloud_quotas.transports.CloudQuotasTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.CloudQuotasTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_cloud_quotas_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.cloudquotas_v1.services.cloud_quotas.transports.CloudQuotasTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.CloudQuotasTransport()
        adc.assert_called_once()


def test_cloud_quotas_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        CloudQuotasClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CloudQuotasGrpcTransport,
        transports.CloudQuotasGrpcAsyncIOTransport,
    ],
)
def test_cloud_quotas_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CloudQuotasGrpcTransport,
        transports.CloudQuotasGrpcAsyncIOTransport,
        transports.CloudQuotasRestTransport,
    ],
)
def test_cloud_quotas_transport_auth_gdch_credentials(transport_class):
    host = "https://language.com"
    api_audience_tests = [None, "https://language2.com"]
    api_audience_expect = [host, "https://language2.com"]
    for t, e in zip(api_audience_tests, api_audience_expect):
        with mock.patch.object(google.auth, "default", autospec=True) as adc:
            gdch_mock = mock.MagicMock()
            type(gdch_mock).with_gdch_audience = mock.PropertyMock(
                return_value=gdch_mock
            )
            adc.return_value = (gdch_mock, None)
            transport_class(host=host, api_audience=t)
            gdch_mock.with_gdch_audience.assert_called_once_with(e)


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.CloudQuotasGrpcTransport, grpc_helpers),
        (transports.CloudQuotasGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_cloud_quotas_transport_create_channel(transport_class, grpc_helpers):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])

        create_channel.assert_called_with(
            "cloudquotas.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="cloudquotas.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.CloudQuotasGrpcTransport, transports.CloudQuotasGrpcAsyncIOTransport],
)
def test_cloud_quotas_grpc_transport_client_cert_source_for_mtls(transport_class):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds,
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=None,
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback,
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert, private_key=expected_key
            )


def test_cloud_quotas_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.CloudQuotasRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_cloud_quotas_host_no_port(transport_name):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudquotas.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "cloudquotas.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://cloudquotas.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_cloud_quotas_host_with_port(transport_name):
    client = CloudQuotasClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudquotas.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "cloudquotas.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://cloudquotas.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_cloud_quotas_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = CloudQuotasClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = CloudQuotasClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.list_quota_infos._session
    session2 = client2.transport.list_quota_infos._session
    assert session1 != session2
    session1 = client1.transport.get_quota_info._session
    session2 = client2.transport.get_quota_info._session
    assert session1 != session2
    session1 = client1.transport.list_quota_preferences._session
    session2 = client2.transport.list_quota_preferences._session
    assert session1 != session2
    session1 = client1.transport.get_quota_preference._session
    session2 = client2.transport.get_quota_preference._session
    assert session1 != session2
    session1 = client1.transport.create_quota_preference._session
    session2 = client2.transport.create_quota_preference._session
    assert session1 != session2
    session1 = client1.transport.update_quota_preference._session
    session2 = client2.transport.update_quota_preference._session
    assert session1 != session2


def test_cloud_quotas_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.CloudQuotasGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_cloud_quotas_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.CloudQuotasGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [transports.CloudQuotasGrpcTransport, transports.CloudQuotasGrpcAsyncIOTransport],
)
def test_cloud_quotas_transport_channel_mtls_with_client_cert_source(transport_class):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [transports.CloudQuotasGrpcTransport, transports.CloudQuotasGrpcAsyncIOTransport],
)
def test_cloud_quotas_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_quota_info_path():
    project = "squid"
    location = "clam"
    service = "whelk"
    quota_info = "octopus"
    expected = "projects/{project}/locations/{location}/services/{service}/quotaInfos/{quota_info}".format(
        project=project,
        location=location,
        service=service,
        quota_info=quota_info,
    )
    actual = CloudQuotasClient.quota_info_path(project, location, service, quota_info)
    assert expected == actual


def test_parse_quota_info_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "service": "cuttlefish",
        "quota_info": "mussel",
    }
    path = CloudQuotasClient.quota_info_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudQuotasClient.parse_quota_info_path(path)
    assert expected == actual


def test_quota_preference_path():
    project = "winkle"
    location = "nautilus"
    quota_preference = "scallop"
    expected = "projects/{project}/locations/{location}/quotaPreferences/{quota_preference}".format(
        project=project,
        location=location,
        quota_preference=quota_preference,
    )
    actual = CloudQuotasClient.quota_preference_path(
        project, location, quota_preference
    )
    assert expected == actual


def test_parse_quota_preference_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "quota_preference": "clam",
    }
    path = CloudQuotasClient.quota_preference_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudQuotasClient.parse_quota_preference_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "whelk"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = CloudQuotasClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = CloudQuotasClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudQuotasClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "oyster"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = CloudQuotasClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = CloudQuotasClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudQuotasClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "cuttlefish"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = CloudQuotasClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = CloudQuotasClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudQuotasClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "winkle"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = CloudQuotasClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = CloudQuotasClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudQuotasClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "scallop"
    location = "abalone"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = CloudQuotasClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = CloudQuotasClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudQuotasClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.CloudQuotasTransport, "_prep_wrapped_messages"
    ) as prep:
        client = CloudQuotasClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.CloudQuotasTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = CloudQuotasClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = CloudQuotasAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close():
    transports = {
        "rest": "_session",
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = CloudQuotasClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        with mock.patch.object(
            type(getattr(client.transport, close_name)), "close"
        ) as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()


def test_client_ctx():
    transports = [
        "rest",
        "grpc",
    ]
    for transport in transports:
        client = CloudQuotasClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()


@pytest.mark.parametrize(
    "client_class,transport_class",
    [
        (CloudQuotasClient, transports.CloudQuotasGrpcTransport),
        (CloudQuotasAsyncClient, transports.CloudQuotasGrpcAsyncIOTransport),
    ],
)
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )
