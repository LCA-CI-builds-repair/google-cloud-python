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
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.oauth2 import service_account
from google.protobuf import json_format
from google.type import expr_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

from google.cloud.contentwarehouse_v1.services.rule_set_service import (
    RuleSetServiceAsyncClient,
    RuleSetServiceClient,
    pagers,
    transports,
)
from google.cloud.contentwarehouse_v1.types import rule_engine, ruleset_service_request


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

    assert RuleSetServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        RuleSetServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        RuleSetServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        RuleSetServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        RuleSetServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        RuleSetServiceClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (RuleSetServiceClient, "grpc"),
        (RuleSetServiceAsyncClient, "grpc_asyncio"),
        (RuleSetServiceClient, "rest"),
    ],
)
def test_rule_set_service_client_from_service_account_info(
    client_class, transport_name
):
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
            "contentwarehouse.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://contentwarehouse.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.RuleSetServiceGrpcTransport, "grpc"),
        (transports.RuleSetServiceGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.RuleSetServiceRestTransport, "rest"),
    ],
)
def test_rule_set_service_client_service_account_always_use_jwt(
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
        (RuleSetServiceClient, "grpc"),
        (RuleSetServiceAsyncClient, "grpc_asyncio"),
        (RuleSetServiceClient, "rest"),
    ],
)
def test_rule_set_service_client_from_service_account_file(
    client_class, transport_name
):
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
            "contentwarehouse.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://contentwarehouse.googleapis.com"
        )


def test_rule_set_service_client_get_transport_class():
    transport = RuleSetServiceClient.get_transport_class()
    available_transports = [
        transports.RuleSetServiceGrpcTransport,
        transports.RuleSetServiceRestTransport,
    ]
    assert transport in available_transports

    transport = RuleSetServiceClient.get_transport_class("grpc")
    assert transport == transports.RuleSetServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (RuleSetServiceClient, transports.RuleSetServiceGrpcTransport, "grpc"),
        (
            RuleSetServiceAsyncClient,
            transports.RuleSetServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (RuleSetServiceClient, transports.RuleSetServiceRestTransport, "rest"),
    ],
)
@mock.patch.object(
    RuleSetServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(RuleSetServiceClient),
)
@mock.patch.object(
    RuleSetServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(RuleSetServiceAsyncClient),
)
def test_rule_set_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(RuleSetServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(RuleSetServiceClient, "get_transport_class") as gtc:
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
        (RuleSetServiceClient, transports.RuleSetServiceGrpcTransport, "grpc", "true"),
        (
            RuleSetServiceAsyncClient,
            transports.RuleSetServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (RuleSetServiceClient, transports.RuleSetServiceGrpcTransport, "grpc", "false"),
        (
            RuleSetServiceAsyncClient,
            transports.RuleSetServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (RuleSetServiceClient, transports.RuleSetServiceRestTransport, "rest", "true"),
        (RuleSetServiceClient, transports.RuleSetServiceRestTransport, "rest", "false"),
    ],
)
@mock.patch.object(
    RuleSetServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(RuleSetServiceClient),
)
@mock.patch.object(
    RuleSetServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(RuleSetServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_rule_set_service_client_mtls_env_auto(
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


@pytest.mark.parametrize(
    "client_class", [RuleSetServiceClient, RuleSetServiceAsyncClient]
)
@mock.patch.object(
    RuleSetServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(RuleSetServiceClient),
)
@mock.patch.object(
    RuleSetServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(RuleSetServiceAsyncClient),
)
def test_rule_set_service_client_get_mtls_endpoint_and_cert_source(client_class):
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
        (RuleSetServiceClient, transports.RuleSetServiceGrpcTransport, "grpc"),
        (
            RuleSetServiceAsyncClient,
            transports.RuleSetServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (RuleSetServiceClient, transports.RuleSetServiceRestTransport, "rest"),
    ],
)
def test_rule_set_service_client_client_options_scopes(
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
        (
            RuleSetServiceClient,
            transports.RuleSetServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            RuleSetServiceAsyncClient,
            transports.RuleSetServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (RuleSetServiceClient, transports.RuleSetServiceRestTransport, "rest", None),
    ],
)
def test_rule_set_service_client_client_options_credentials_file(
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


def test_rule_set_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.contentwarehouse_v1.services.rule_set_service.transports.RuleSetServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = RuleSetServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
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
        (
            RuleSetServiceClient,
            transports.RuleSetServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            RuleSetServiceAsyncClient,
            transports.RuleSetServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_rule_set_service_client_create_channel_credentials_file(
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
            "contentwarehouse.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="contentwarehouse.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        ruleset_service_request.CreateRuleSetRequest,
        dict,
    ],
)
def test_create_rule_set(request_type, transport: str = "grpc"):
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_rule_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule_engine.RuleSet(
            name="name_value",
            description="description_value",
            source="source_value",
        )
        response = client.create_rule_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == ruleset_service_request.CreateRuleSetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, rule_engine.RuleSet)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.source == "source_value"


def test_create_rule_set_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_rule_set), "__call__") as call:
        client.create_rule_set()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == ruleset_service_request.CreateRuleSetRequest()


@pytest.mark.asyncio
async def test_create_rule_set_async(
    transport: str = "grpc_asyncio",
    request_type=ruleset_service_request.CreateRuleSetRequest,
):
    client = RuleSetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_rule_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            rule_engine.RuleSet(
                name="name_value",
                description="description_value",
                source="source_value",
            )
        )
        response = await client.create_rule_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == ruleset_service_request.CreateRuleSetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, rule_engine.RuleSet)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.source == "source_value"


@pytest.mark.asyncio
async def test_create_rule_set_async_from_dict():
    await test_create_rule_set_async(request_type=dict)


def test_create_rule_set_field_headers():
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = ruleset_service_request.CreateRuleSetRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_rule_set), "__call__") as call:
        call.return_value = rule_engine.RuleSet()
        client.create_rule_set(request)

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
async def test_create_rule_set_field_headers_async():
    client = RuleSetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = ruleset_service_request.CreateRuleSetRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_rule_set), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(rule_engine.RuleSet())
        await client.create_rule_set(request)

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


def test_create_rule_set_flattened():
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_rule_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule_engine.RuleSet()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_rule_set(
            parent="parent_value",
            rule_set=rule_engine.RuleSet(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].rule_set
        mock_val = rule_engine.RuleSet(name="name_value")
        assert arg == mock_val


def test_create_rule_set_flattened_error():
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_rule_set(
            ruleset_service_request.CreateRuleSetRequest(),
            parent="parent_value",
            rule_set=rule_engine.RuleSet(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_rule_set_flattened_async():
    client = RuleSetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_rule_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule_engine.RuleSet()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(rule_engine.RuleSet())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_rule_set(
            parent="parent_value",
            rule_set=rule_engine.RuleSet(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].rule_set
        mock_val = rule_engine.RuleSet(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_rule_set_flattened_error_async():
    client = RuleSetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_rule_set(
            ruleset_service_request.CreateRuleSetRequest(),
            parent="parent_value",
            rule_set=rule_engine.RuleSet(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        ruleset_service_request.GetRuleSetRequest,
        dict,
    ],
)
def test_get_rule_set(request_type, transport: str = "grpc"):
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_rule_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule_engine.RuleSet(
            name="name_value",
            description="description_value",
            source="source_value",
        )
        response = client.get_rule_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == ruleset_service_request.GetRuleSetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, rule_engine.RuleSet)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.source == "source_value"


def test_get_rule_set_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_rule_set), "__call__") as call:
        client.get_rule_set()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == ruleset_service_request.GetRuleSetRequest()


@pytest.mark.asyncio
async def test_get_rule_set_async(
    transport: str = "grpc_asyncio",
    request_type=ruleset_service_request.GetRuleSetRequest,
):
    client = RuleSetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_rule_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            rule_engine.RuleSet(
                name="name_value",
                description="description_value",
                source="source_value",
            )
        )
        response = await client.get_rule_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == ruleset_service_request.GetRuleSetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, rule_engine.RuleSet)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.source == "source_value"


@pytest.mark.asyncio
async def test_get_rule_set_async_from_dict():
    await test_get_rule_set_async(request_type=dict)


def test_get_rule_set_field_headers():
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = ruleset_service_request.GetRuleSetRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_rule_set), "__call__") as call:
        call.return_value = rule_engine.RuleSet()
        client.get_rule_set(request)

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
async def test_get_rule_set_field_headers_async():
    client = RuleSetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = ruleset_service_request.GetRuleSetRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_rule_set), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(rule_engine.RuleSet())
        await client.get_rule_set(request)

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


def test_get_rule_set_flattened():
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_rule_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule_engine.RuleSet()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_rule_set(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_rule_set_flattened_error():
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_rule_set(
            ruleset_service_request.GetRuleSetRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_rule_set_flattened_async():
    client = RuleSetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_rule_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule_engine.RuleSet()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(rule_engine.RuleSet())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_rule_set(
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
async def test_get_rule_set_flattened_error_async():
    client = RuleSetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_rule_set(
            ruleset_service_request.GetRuleSetRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        ruleset_service_request.UpdateRuleSetRequest,
        dict,
    ],
)
def test_update_rule_set(request_type, transport: str = "grpc"):
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_rule_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule_engine.RuleSet(
            name="name_value",
            description="description_value",
            source="source_value",
        )
        response = client.update_rule_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == ruleset_service_request.UpdateRuleSetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, rule_engine.RuleSet)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.source == "source_value"


def test_update_rule_set_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_rule_set), "__call__") as call:
        client.update_rule_set()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == ruleset_service_request.UpdateRuleSetRequest()


@pytest.mark.asyncio
async def test_update_rule_set_async(
    transport: str = "grpc_asyncio",
    request_type=ruleset_service_request.UpdateRuleSetRequest,
):
    client = RuleSetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_rule_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            rule_engine.RuleSet(
                name="name_value",
                description="description_value",
                source="source_value",
            )
        )
        response = await client.update_rule_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == ruleset_service_request.UpdateRuleSetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, rule_engine.RuleSet)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.source == "source_value"


@pytest.mark.asyncio
async def test_update_rule_set_async_from_dict():
    await test_update_rule_set_async(request_type=dict)


def test_update_rule_set_field_headers():
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = ruleset_service_request.UpdateRuleSetRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_rule_set), "__call__") as call:
        call.return_value = rule_engine.RuleSet()
        client.update_rule_set(request)

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
async def test_update_rule_set_field_headers_async():
    client = RuleSetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = ruleset_service_request.UpdateRuleSetRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_rule_set), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(rule_engine.RuleSet())
        await client.update_rule_set(request)

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


def test_update_rule_set_flattened():
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_rule_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule_engine.RuleSet()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_rule_set(
            name="name_value",
            rule_set=rule_engine.RuleSet(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].rule_set
        mock_val = rule_engine.RuleSet(name="name_value")
        assert arg == mock_val


def test_update_rule_set_flattened_error():
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_rule_set(
            ruleset_service_request.UpdateRuleSetRequest(),
            name="name_value",
            rule_set=rule_engine.RuleSet(name="name_value"),
        )


@pytest.mark.asyncio
async def test_update_rule_set_flattened_async():
    client = RuleSetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_rule_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = rule_engine.RuleSet()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(rule_engine.RuleSet())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_rule_set(
            name="name_value",
            rule_set=rule_engine.RuleSet(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].rule_set
        mock_val = rule_engine.RuleSet(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_rule_set_flattened_error_async():
    client = RuleSetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_rule_set(
            ruleset_service_request.UpdateRuleSetRequest(),
            name="name_value",
            rule_set=rule_engine.RuleSet(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        ruleset_service_request.DeleteRuleSetRequest,
        dict,
    ],
)
def test_delete_rule_set(request_type, transport: str = "grpc"):
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_rule_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_rule_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == ruleset_service_request.DeleteRuleSetRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_rule_set_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_rule_set), "__call__") as call:
        client.delete_rule_set()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == ruleset_service_request.DeleteRuleSetRequest()


@pytest.mark.asyncio
async def test_delete_rule_set_async(
    transport: str = "grpc_asyncio",
    request_type=ruleset_service_request.DeleteRuleSetRequest,
):
    client = RuleSetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_rule_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_rule_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == ruleset_service_request.DeleteRuleSetRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_rule_set_async_from_dict():
    await test_delete_rule_set_async(request_type=dict)


def test_delete_rule_set_field_headers():
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = ruleset_service_request.DeleteRuleSetRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_rule_set), "__call__") as call:
        call.return_value = None
        client.delete_rule_set(request)

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
async def test_delete_rule_set_field_headers_async():
    client = RuleSetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = ruleset_service_request.DeleteRuleSetRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_rule_set), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_rule_set(request)

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


def test_delete_rule_set_flattened():
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_rule_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_rule_set(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_rule_set_flattened_error():
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_rule_set(
            ruleset_service_request.DeleteRuleSetRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_rule_set_flattened_async():
    client = RuleSetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_rule_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_rule_set(
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
async def test_delete_rule_set_flattened_error_async():
    client = RuleSetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_rule_set(
            ruleset_service_request.DeleteRuleSetRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        ruleset_service_request.ListRuleSetsRequest,
        dict,
    ],
)
def test_list_rule_sets(request_type, transport: str = "grpc"):
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_rule_sets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = ruleset_service_request.ListRuleSetsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_rule_sets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == ruleset_service_request.ListRuleSetsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRuleSetsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_rule_sets_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_rule_sets), "__call__") as call:
        client.list_rule_sets()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == ruleset_service_request.ListRuleSetsRequest()


@pytest.mark.asyncio
async def test_list_rule_sets_async(
    transport: str = "grpc_asyncio",
    request_type=ruleset_service_request.ListRuleSetsRequest,
):
    client = RuleSetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_rule_sets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            ruleset_service_request.ListRuleSetsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_rule_sets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == ruleset_service_request.ListRuleSetsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRuleSetsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_rule_sets_async_from_dict():
    await test_list_rule_sets_async(request_type=dict)


def test_list_rule_sets_field_headers():
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = ruleset_service_request.ListRuleSetsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_rule_sets), "__call__") as call:
        call.return_value = ruleset_service_request.ListRuleSetsResponse()
        client.list_rule_sets(request)

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
async def test_list_rule_sets_field_headers_async():
    client = RuleSetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = ruleset_service_request.ListRuleSetsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_rule_sets), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            ruleset_service_request.ListRuleSetsResponse()
        )
        await client.list_rule_sets(request)

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


def test_list_rule_sets_flattened():
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_rule_sets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = ruleset_service_request.ListRuleSetsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_rule_sets(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_rule_sets_flattened_error():
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_rule_sets(
            ruleset_service_request.ListRuleSetsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_rule_sets_flattened_async():
    client = RuleSetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_rule_sets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = ruleset_service_request.ListRuleSetsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            ruleset_service_request.ListRuleSetsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_rule_sets(
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
async def test_list_rule_sets_flattened_error_async():
    client = RuleSetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_rule_sets(
            ruleset_service_request.ListRuleSetsRequest(),
            parent="parent_value",
        )


def test_list_rule_sets_pager(transport_name: str = "grpc"):
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_rule_sets), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            ruleset_service_request.ListRuleSetsResponse(
                rule_sets=[
                    rule_engine.RuleSet(),
                    rule_engine.RuleSet(),
                    rule_engine.RuleSet(),
                ],
                next_page_token="abc",
            ),
            ruleset_service_request.ListRuleSetsResponse(
                rule_sets=[],
                next_page_token="def",
            ),
            ruleset_service_request.ListRuleSetsResponse(
                rule_sets=[
                    rule_engine.RuleSet(),
                ],
                next_page_token="ghi",
            ),
            ruleset_service_request.ListRuleSetsResponse(
                rule_sets=[
                    rule_engine.RuleSet(),
                    rule_engine.RuleSet(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_rule_sets(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, rule_engine.RuleSet) for i in results)


def test_list_rule_sets_pages(transport_name: str = "grpc"):
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_rule_sets), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            ruleset_service_request.ListRuleSetsResponse(
                rule_sets=[
                    rule_engine.RuleSet(),
                    rule_engine.RuleSet(),
                    rule_engine.RuleSet(),
                ],
                next_page_token="abc",
            ),
            ruleset_service_request.ListRuleSetsResponse(
                rule_sets=[],
                next_page_token="def",
            ),
            ruleset_service_request.ListRuleSetsResponse(
                rule_sets=[
                    rule_engine.RuleSet(),
                ],
                next_page_token="ghi",
            ),
            ruleset_service_request.ListRuleSetsResponse(
                rule_sets=[
                    rule_engine.RuleSet(),
                    rule_engine.RuleSet(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_rule_sets(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_rule_sets_async_pager():
    client = RuleSetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_sets), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            ruleset_service_request.ListRuleSetsResponse(
                rule_sets=[
                    rule_engine.RuleSet(),
                    rule_engine.RuleSet(),
                    rule_engine.RuleSet(),
                ],
                next_page_token="abc",
            ),
            ruleset_service_request.ListRuleSetsResponse(
                rule_sets=[],
                next_page_token="def",
            ),
            ruleset_service_request.ListRuleSetsResponse(
                rule_sets=[
                    rule_engine.RuleSet(),
                ],
                next_page_token="ghi",
            ),
            ruleset_service_request.ListRuleSetsResponse(
                rule_sets=[
                    rule_engine.RuleSet(),
                    rule_engine.RuleSet(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_rule_sets(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, rule_engine.RuleSet) for i in responses)


@pytest.mark.asyncio
async def test_list_rule_sets_async_pages():
    client = RuleSetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_rule_sets), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            ruleset_service_request.ListRuleSetsResponse(
                rule_sets=[
                    rule_engine.RuleSet(),
                    rule_engine.RuleSet(),
                    rule_engine.RuleSet(),
                ],
                next_page_token="abc",
            ),
            ruleset_service_request.ListRuleSetsResponse(
                rule_sets=[],
                next_page_token="def",
            ),
            ruleset_service_request.ListRuleSetsResponse(
                rule_sets=[
                    rule_engine.RuleSet(),
                ],
                next_page_token="ghi",
            ),
            ruleset_service_request.ListRuleSetsResponse(
                rule_sets=[
                    rule_engine.RuleSet(),
                    rule_engine.RuleSet(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_rule_sets(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        ruleset_service_request.CreateRuleSetRequest,
        dict,
    ],
)
def test_create_rule_set_rest(request_type):
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["rule_set"] = {
        "name": "name_value",
        "description": "description_value",
        "source": "source_value",
        "rules": [
            {
                "description": "description_value",
                "rule_id": "rule_id_value",
                "trigger_type": 1,
                "condition": "condition_value",
                "actions": [
                    {
                        "action_id": "action_id_value",
                        "access_control": {
                            "operation_type": 1,
                            "policy": {
                                "version": 774,
                                "bindings": [
                                    {
                                        "role": "role_value",
                                        "members": ["members_value1", "members_value2"],
                                        "condition": {
                                            "expression": "expression_value",
                                            "title": "title_value",
                                            "description": "description_value",
                                            "location": "location_value",
                                        },
                                    }
                                ],
                                "audit_configs": [
                                    {
                                        "service": "service_value",
                                        "audit_log_configs": [
                                            {
                                                "log_type": 1,
                                                "exempted_members": [
                                                    "exempted_members_value1",
                                                    "exempted_members_value2",
                                                ],
                                            }
                                        ],
                                    }
                                ],
                                "etag": b"etag_blob",
                            },
                        },
                        "data_validation": {"conditions": {}},
                        "data_update": {"entries": {}},
                        "add_to_folder": {
                            "folders": ["folders_value1", "folders_value2"]
                        },
                        "publish_to_pub_sub": {
                            "topic_id": "topic_id_value",
                            "messages": ["messages_value1", "messages_value2"],
                        },
                        "remove_from_folder_action": {
                            "condition": "condition_value",
                            "folder": "folder_value",
                        },
                        "delete_document_action": {"enable_hard_delete": True},
                    }
                ],
            }
        ],
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = ruleset_service_request.CreateRuleSetRequest.meta.fields["rule_set"]

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
    for field, value in request_init["rule_set"].items():  # pragma: NO COVER
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
                for i in range(0, len(request_init["rule_set"][field])):
                    del request_init["rule_set"][field][i][subfield]
            else:
                del request_init["rule_set"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = rule_engine.RuleSet(
            name="name_value",
            description="description_value",
            source="source_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = rule_engine.RuleSet.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_rule_set(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, rule_engine.RuleSet)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.source == "source_value"


def test_create_rule_set_rest_required_fields(
    request_type=ruleset_service_request.CreateRuleSetRequest,
):
    transport_class = transports.RuleSetServiceRestTransport

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
    ).create_rule_set._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_rule_set._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = rule_engine.RuleSet()
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
            return_value = rule_engine.RuleSet.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_rule_set(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_rule_set_rest_unset_required_fields():
    transport = transports.RuleSetServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_rule_set._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "ruleSet",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_rule_set_rest_interceptors(null_interceptor):
    transport = transports.RuleSetServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.RuleSetServiceRestInterceptor(),
    )
    client = RuleSetServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RuleSetServiceRestInterceptor, "post_create_rule_set"
    ) as post, mock.patch.object(
        transports.RuleSetServiceRestInterceptor, "pre_create_rule_set"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = ruleset_service_request.CreateRuleSetRequest.pb(
            ruleset_service_request.CreateRuleSetRequest()
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
        req.return_value._content = rule_engine.RuleSet.to_json(rule_engine.RuleSet())

        request = ruleset_service_request.CreateRuleSetRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = rule_engine.RuleSet()

        client.create_rule_set(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_rule_set_rest_bad_request(
    transport: str = "rest", request_type=ruleset_service_request.CreateRuleSetRequest
):
    client = RuleSetServiceClient(
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
        client.create_rule_set(request)


def test_create_rule_set_rest_flattened():
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = rule_engine.RuleSet()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            rule_set=rule_engine.RuleSet(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = rule_engine.RuleSet.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_rule_set(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/ruleSets" % client.transport._host,
            args[1],
        )


def test_create_rule_set_rest_flattened_error(transport: str = "rest"):
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_rule_set(
            ruleset_service_request.CreateRuleSetRequest(),
            parent="parent_value",
            rule_set=rule_engine.RuleSet(name="name_value"),
        )


def test_create_rule_set_rest_error():
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        ruleset_service_request.GetRuleSetRequest,
        dict,
    ],
)
def test_get_rule_set_rest(request_type):
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/ruleSets/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = rule_engine.RuleSet(
            name="name_value",
            description="description_value",
            source="source_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = rule_engine.RuleSet.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_rule_set(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, rule_engine.RuleSet)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.source == "source_value"


def test_get_rule_set_rest_required_fields(
    request_type=ruleset_service_request.GetRuleSetRequest,
):
    transport_class = transports.RuleSetServiceRestTransport

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
    ).get_rule_set._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_rule_set._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = rule_engine.RuleSet()
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
            return_value = rule_engine.RuleSet.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_rule_set(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_rule_set_rest_unset_required_fields():
    transport = transports.RuleSetServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_rule_set._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_rule_set_rest_interceptors(null_interceptor):
    transport = transports.RuleSetServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.RuleSetServiceRestInterceptor(),
    )
    client = RuleSetServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RuleSetServiceRestInterceptor, "post_get_rule_set"
    ) as post, mock.patch.object(
        transports.RuleSetServiceRestInterceptor, "pre_get_rule_set"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = ruleset_service_request.GetRuleSetRequest.pb(
            ruleset_service_request.GetRuleSetRequest()
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
        req.return_value._content = rule_engine.RuleSet.to_json(rule_engine.RuleSet())

        request = ruleset_service_request.GetRuleSetRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = rule_engine.RuleSet()

        client.get_rule_set(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_rule_set_rest_bad_request(
    transport: str = "rest", request_type=ruleset_service_request.GetRuleSetRequest
):
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/ruleSets/sample3"}
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
        client.get_rule_set(request)


def test_get_rule_set_rest_flattened():
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = rule_engine.RuleSet()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/ruleSets/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = rule_engine.RuleSet.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_rule_set(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/ruleSets/*}" % client.transport._host,
            args[1],
        )


def test_get_rule_set_rest_flattened_error(transport: str = "rest"):
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_rule_set(
            ruleset_service_request.GetRuleSetRequest(),
            name="name_value",
        )


def test_get_rule_set_rest_error():
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        ruleset_service_request.UpdateRuleSetRequest,
        dict,
    ],
)
def test_update_rule_set_rest(request_type):
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/ruleSets/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = rule_engine.RuleSet(
            name="name_value",
            description="description_value",
            source="source_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = rule_engine.RuleSet.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_rule_set(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, rule_engine.RuleSet)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.source == "source_value"


def test_update_rule_set_rest_required_fields(
    request_type=ruleset_service_request.UpdateRuleSetRequest,
):
    transport_class = transports.RuleSetServiceRestTransport

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
    ).update_rule_set._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_rule_set._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = rule_engine.RuleSet()
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
            return_value = rule_engine.RuleSet.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_rule_set(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_rule_set_rest_unset_required_fields():
    transport = transports.RuleSetServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_rule_set._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "name",
                "ruleSet",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_rule_set_rest_interceptors(null_interceptor):
    transport = transports.RuleSetServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.RuleSetServiceRestInterceptor(),
    )
    client = RuleSetServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RuleSetServiceRestInterceptor, "post_update_rule_set"
    ) as post, mock.patch.object(
        transports.RuleSetServiceRestInterceptor, "pre_update_rule_set"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = ruleset_service_request.UpdateRuleSetRequest.pb(
            ruleset_service_request.UpdateRuleSetRequest()
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
        req.return_value._content = rule_engine.RuleSet.to_json(rule_engine.RuleSet())

        request = ruleset_service_request.UpdateRuleSetRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = rule_engine.RuleSet()

        client.update_rule_set(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_rule_set_rest_bad_request(
    transport: str = "rest", request_type=ruleset_service_request.UpdateRuleSetRequest
):
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/ruleSets/sample3"}
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
        client.update_rule_set(request)


def test_update_rule_set_rest_flattened():
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = rule_engine.RuleSet()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/ruleSets/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
            rule_set=rule_engine.RuleSet(name="name_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = rule_engine.RuleSet.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_rule_set(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/ruleSets/*}" % client.transport._host,
            args[1],
        )


def test_update_rule_set_rest_flattened_error(transport: str = "rest"):
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_rule_set(
            ruleset_service_request.UpdateRuleSetRequest(),
            name="name_value",
            rule_set=rule_engine.RuleSet(name="name_value"),
        )


def test_update_rule_set_rest_error():
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        ruleset_service_request.DeleteRuleSetRequest,
        dict,
    ],
)
def test_delete_rule_set_rest(request_type):
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/ruleSets/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_rule_set(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_rule_set_rest_required_fields(
    request_type=ruleset_service_request.DeleteRuleSetRequest,
):
    transport_class = transports.RuleSetServiceRestTransport

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
    ).delete_rule_set._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_rule_set._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = None
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
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = ""

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_rule_set(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_rule_set_rest_unset_required_fields():
    transport = transports.RuleSetServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_rule_set._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_rule_set_rest_interceptors(null_interceptor):
    transport = transports.RuleSetServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.RuleSetServiceRestInterceptor(),
    )
    client = RuleSetServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RuleSetServiceRestInterceptor, "pre_delete_rule_set"
    ) as pre:
        pre.assert_not_called()
        pb_message = ruleset_service_request.DeleteRuleSetRequest.pb(
            ruleset_service_request.DeleteRuleSetRequest()
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

        request = ruleset_service_request.DeleteRuleSetRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_rule_set(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_rule_set_rest_bad_request(
    transport: str = "rest", request_type=ruleset_service_request.DeleteRuleSetRequest
):
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/ruleSets/sample3"}
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
        client.delete_rule_set(request)


def test_delete_rule_set_rest_flattened():
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/ruleSets/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_rule_set(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/ruleSets/*}" % client.transport._host,
            args[1],
        )


def test_delete_rule_set_rest_flattened_error(transport: str = "rest"):
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_rule_set(
            ruleset_service_request.DeleteRuleSetRequest(),
            name="name_value",
        )


def test_delete_rule_set_rest_error():
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        ruleset_service_request.ListRuleSetsRequest,
        dict,
    ],
)
def test_list_rule_sets_rest(request_type):
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = ruleset_service_request.ListRuleSetsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = ruleset_service_request.ListRuleSetsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_rule_sets(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRuleSetsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_rule_sets_rest_required_fields(
    request_type=ruleset_service_request.ListRuleSetsRequest,
):
    transport_class = transports.RuleSetServiceRestTransport

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
    ).list_rule_sets._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_rule_sets._get_unset_required_fields(jsonified_request)
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

    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = ruleset_service_request.ListRuleSetsResponse()
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
            return_value = ruleset_service_request.ListRuleSetsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_rule_sets(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_rule_sets_rest_unset_required_fields():
    transport = transports.RuleSetServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_rule_sets._get_unset_required_fields({})
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
def test_list_rule_sets_rest_interceptors(null_interceptor):
    transport = transports.RuleSetServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.RuleSetServiceRestInterceptor(),
    )
    client = RuleSetServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.RuleSetServiceRestInterceptor, "post_list_rule_sets"
    ) as post, mock.patch.object(
        transports.RuleSetServiceRestInterceptor, "pre_list_rule_sets"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = ruleset_service_request.ListRuleSetsRequest.pb(
            ruleset_service_request.ListRuleSetsRequest()
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
        req.return_value._content = (
            ruleset_service_request.ListRuleSetsResponse.to_json(
                ruleset_service_request.ListRuleSetsResponse()
            )
        )

        request = ruleset_service_request.ListRuleSetsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = ruleset_service_request.ListRuleSetsResponse()

        client.list_rule_sets(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_rule_sets_rest_bad_request(
    transport: str = "rest", request_type=ruleset_service_request.ListRuleSetsRequest
):
    client = RuleSetServiceClient(
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
        client.list_rule_sets(request)


def test_list_rule_sets_rest_flattened():
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = ruleset_service_request.ListRuleSetsResponse()

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
        return_value = ruleset_service_request.ListRuleSetsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_rule_sets(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/ruleSets" % client.transport._host,
            args[1],
        )


def test_list_rule_sets_rest_flattened_error(transport: str = "rest"):
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_rule_sets(
            ruleset_service_request.ListRuleSetsRequest(),
            parent="parent_value",
        )


def test_list_rule_sets_rest_pager(transport: str = "rest"):
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            ruleset_service_request.ListRuleSetsResponse(
                rule_sets=[
                    rule_engine.RuleSet(),
                    rule_engine.RuleSet(),
                    rule_engine.RuleSet(),
                ],
                next_page_token="abc",
            ),
            ruleset_service_request.ListRuleSetsResponse(
                rule_sets=[],
                next_page_token="def",
            ),
            ruleset_service_request.ListRuleSetsResponse(
                rule_sets=[
                    rule_engine.RuleSet(),
                ],
                next_page_token="ghi",
            ),
            ruleset_service_request.ListRuleSetsResponse(
                rule_sets=[
                    rule_engine.RuleSet(),
                    rule_engine.RuleSet(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            ruleset_service_request.ListRuleSetsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_rule_sets(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, rule_engine.RuleSet) for i in results)

        pages = list(client.list_rule_sets(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.RuleSetServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = RuleSetServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.RuleSetServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = RuleSetServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.RuleSetServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = RuleSetServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = RuleSetServiceClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.RuleSetServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = RuleSetServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.RuleSetServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = RuleSetServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.RuleSetServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.RuleSetServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.RuleSetServiceGrpcTransport,
        transports.RuleSetServiceGrpcAsyncIOTransport,
        transports.RuleSetServiceRestTransport,
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
    transport = RuleSetServiceClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.RuleSetServiceGrpcTransport,
    )


def test_rule_set_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.RuleSetServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_rule_set_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.contentwarehouse_v1.services.rule_set_service.transports.RuleSetServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.RuleSetServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_rule_set",
        "get_rule_set",
        "update_rule_set",
        "delete_rule_set",
        "list_rule_sets",
        "get_operation",
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


def test_rule_set_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.contentwarehouse_v1.services.rule_set_service.transports.RuleSetServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.RuleSetServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_rule_set_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.contentwarehouse_v1.services.rule_set_service.transports.RuleSetServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.RuleSetServiceTransport()
        adc.assert_called_once()


def test_rule_set_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        RuleSetServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.RuleSetServiceGrpcTransport,
        transports.RuleSetServiceGrpcAsyncIOTransport,
    ],
)
def test_rule_set_service_transport_auth_adc(transport_class):
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
        transports.RuleSetServiceGrpcTransport,
        transports.RuleSetServiceGrpcAsyncIOTransport,
        transports.RuleSetServiceRestTransport,
    ],
)
def test_rule_set_service_transport_auth_gdch_credentials(transport_class):
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
        (transports.RuleSetServiceGrpcTransport, grpc_helpers),
        (transports.RuleSetServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_rule_set_service_transport_create_channel(transport_class, grpc_helpers):
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
            "contentwarehouse.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="contentwarehouse.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.RuleSetServiceGrpcTransport,
        transports.RuleSetServiceGrpcAsyncIOTransport,
    ],
)
def test_rule_set_service_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_rule_set_service_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.RuleSetServiceRestTransport(
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
def test_rule_set_service_host_no_port(transport_name):
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="contentwarehouse.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "contentwarehouse.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://contentwarehouse.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_rule_set_service_host_with_port(transport_name):
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="contentwarehouse.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "contentwarehouse.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://contentwarehouse.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_rule_set_service_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = RuleSetServiceClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = RuleSetServiceClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.create_rule_set._session
    session2 = client2.transport.create_rule_set._session
    assert session1 != session2
    session1 = client1.transport.get_rule_set._session
    session2 = client2.transport.get_rule_set._session
    assert session1 != session2
    session1 = client1.transport.update_rule_set._session
    session2 = client2.transport.update_rule_set._session
    assert session1 != session2
    session1 = client1.transport.delete_rule_set._session
    session2 = client2.transport.delete_rule_set._session
    assert session1 != session2
    session1 = client1.transport.list_rule_sets._session
    session2 = client2.transport.list_rule_sets._session
    assert session1 != session2


def test_rule_set_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.RuleSetServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_rule_set_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.RuleSetServiceGrpcAsyncIOTransport(
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
    [
        transports.RuleSetServiceGrpcTransport,
        transports.RuleSetServiceGrpcAsyncIOTransport,
    ],
)
def test_rule_set_service_transport_channel_mtls_with_client_cert_source(
    transport_class,
):
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
    [
        transports.RuleSetServiceGrpcTransport,
        transports.RuleSetServiceGrpcAsyncIOTransport,
    ],
)
def test_rule_set_service_transport_channel_mtls_with_adc(transport_class):
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


def test_document_path():
    project = "squid"
    location = "clam"
    document = "whelk"
    expected = "projects/{project}/locations/{location}/documents/{document}".format(
        project=project,
        location=location,
        document=document,
    )
    actual = RuleSetServiceClient.document_path(project, location, document)
    assert expected == actual


def test_parse_document_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "document": "nudibranch",
    }
    path = RuleSetServiceClient.document_path(**expected)

    # Check that the path construction is reversible.
    actual = RuleSetServiceClient.parse_document_path(path)
    assert expected == actual


def test_location_path():
    project = "cuttlefish"
    location = "mussel"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = RuleSetServiceClient.location_path(project, location)
    assert expected == actual


def test_parse_location_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
    }
    path = RuleSetServiceClient.location_path(**expected)

    # Check that the path construction is reversible.
    actual = RuleSetServiceClient.parse_location_path(path)
    assert expected == actual


def test_rule_set_path():
    project = "scallop"
    location = "abalone"
    rule_set = "squid"
    expected = "projects/{project}/locations/{location}/ruleSets/{rule_set}".format(
        project=project,
        location=location,
        rule_set=rule_set,
    )
    actual = RuleSetServiceClient.rule_set_path(project, location, rule_set)
    assert expected == actual


def test_parse_rule_set_path():
    expected = {
        "project": "clam",
        "location": "whelk",
        "rule_set": "octopus",
    }
    path = RuleSetServiceClient.rule_set_path(**expected)

    # Check that the path construction is reversible.
    actual = RuleSetServiceClient.parse_rule_set_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "oyster"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = RuleSetServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nudibranch",
    }
    path = RuleSetServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = RuleSetServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "cuttlefish"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = RuleSetServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "mussel",
    }
    path = RuleSetServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = RuleSetServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "winkle"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = RuleSetServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nautilus",
    }
    path = RuleSetServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = RuleSetServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "scallop"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = RuleSetServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "abalone",
    }
    path = RuleSetServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = RuleSetServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "squid"
    location = "clam"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = RuleSetServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
    }
    path = RuleSetServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = RuleSetServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.RuleSetServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = RuleSetServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.RuleSetServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = RuleSetServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = RuleSetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_get_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.GetOperationRequest
):
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2/operations/sample3"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.GetOperationRequest,
        dict,
    ],
)
def test_get_operation_rest(request_type):
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2/operations/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.get_operation(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_get_operation(transport: str = "grpc"):
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()
        response = client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


@pytest.mark.asyncio
async def test_get_operation_async(transport: str = "grpc_asyncio"):
    client = RuleSetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_get_operation_field_headers():
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = operations_pb2.Operation()

        client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_operation_field_headers_async():
    client = RuleSetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        await client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_get_operation_from_dict():
    client = RuleSetServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()

        response = client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_get_operation_from_dict_async():
    client = RuleSetServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_transport_close():
    transports = {
        "rest": "_session",
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = RuleSetServiceClient(
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
        client = RuleSetServiceClient(
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
        (RuleSetServiceClient, transports.RuleSetServiceGrpcTransport),
        (RuleSetServiceAsyncClient, transports.RuleSetServiceGrpcAsyncIOTransport),
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
