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
from collections import OrderedDict
import functools
import re
from typing import (
    Dict,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry_async as retries
from google.api_core.client_options import ClientOptions
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.tasks_v2beta2 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.AsyncRetry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.AsyncRetry, object]  # type: ignore

from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.tasks_v2beta2.services.cloud_tasks import pagers
from google.cloud.tasks_v2beta2.types import cloudtasks
from google.cloud.tasks_v2beta2.types import queue
from google.cloud.tasks_v2beta2.types import queue as gct_queue
from google.cloud.tasks_v2beta2.types import target
from google.cloud.tasks_v2beta2.types import task
from google.cloud.tasks_v2beta2.types import task as gct_task

from .client import CloudTasksClient
from .transports.base import DEFAULT_CLIENT_INFO, CloudTasksTransport
from .transports.grpc_asyncio import CloudTasksGrpcAsyncIOTransport


class CloudTasksAsyncClient:
    """Cloud Tasks allows developers to manage the execution of
    background work in their applications.
    """

    _client: CloudTasksClient

    DEFAULT_ENDPOINT = CloudTasksClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = CloudTasksClient.DEFAULT_MTLS_ENDPOINT

    queue_path = staticmethod(CloudTasksClient.queue_path)
    parse_queue_path = staticmethod(CloudTasksClient.parse_queue_path)
    task_path = staticmethod(CloudTasksClient.task_path)
    parse_task_path = staticmethod(CloudTasksClient.parse_task_path)
    common_billing_account_path = staticmethod(
        CloudTasksClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        CloudTasksClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(CloudTasksClient.common_folder_path)
    parse_common_folder_path = staticmethod(CloudTasksClient.parse_common_folder_path)
    common_organization_path = staticmethod(CloudTasksClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        CloudTasksClient.parse_common_organization_path
    )
    common_project_path = staticmethod(CloudTasksClient.common_project_path)
    parse_common_project_path = staticmethod(CloudTasksClient.parse_common_project_path)
    common_location_path = staticmethod(CloudTasksClient.common_location_path)
    parse_common_location_path = staticmethod(
        CloudTasksClient.parse_common_location_path
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            CloudTasksAsyncClient: The constructed client.
        """
        return CloudTasksClient.from_service_account_info.__func__(CloudTasksAsyncClient, info, *args, **kwargs)  # type: ignore

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            CloudTasksAsyncClient: The constructed client.
        """
        return CloudTasksClient.from_service_account_file.__func__(CloudTasksAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[ClientOptions] = None
    ):
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variable is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """
        return CloudTasksClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> CloudTasksTransport:
        """Returns the transport used by the client instance.

        Returns:
            CloudTasksTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(CloudTasksClient).get_transport_class, type(CloudTasksClient)
    )

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, CloudTasksTransport] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the cloud tasks client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.CloudTasksTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = CloudTasksClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_queues(
        self,
        request: Optional[Union[cloudtasks.ListQueuesRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListQueuesAsyncPager:
        r"""Lists queues.

        Queues are returned in lexicographical order.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import tasks_v2beta2

            async def sample_list_queues():
                # Create a client
                client = tasks_v2beta2.CloudTasksAsyncClient()

                # Initialize request argument(s)
                request = tasks_v2beta2.ListQueuesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_queues(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.tasks_v2beta2.types.ListQueuesRequest, dict]]):
                The request object. Request message for
                [ListQueues][google.cloud.tasks.v2beta2.CloudTasks.ListQueues].
            parent (:class:`str`):
                Required. The location name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tasks_v2beta2.services.cloud_tasks.pagers.ListQueuesAsyncPager:
                Response message for
                   [ListQueues][google.cloud.tasks.v2beta2.CloudTasks.ListQueues].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudtasks.ListQueuesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_queues,
            default_retry=retries.AsyncRetry(
                initial=0.1,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=20.0,
            ),
            default_timeout=20.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListQueuesAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_queue(
        self,
        request: Optional[Union[cloudtasks.GetQueueRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> queue.Queue:
        r"""Gets a queue.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import tasks_v2beta2

            async def sample_get_queue():
                # Create a client
                client = tasks_v2beta2.CloudTasksAsyncClient()

                # Initialize request argument(s)
                request = tasks_v2beta2.GetQueueRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_queue(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.tasks_v2beta2.types.GetQueueRequest, dict]]):
                The request object. Request message for
                [GetQueue][google.cloud.tasks.v2beta2.CloudTasks.GetQueue].
            name (:class:`str`):
                Required. The resource name of the queue. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tasks_v2beta2.types.Queue:
                A queue is a container of related
                tasks. Queues are configured to manage
                how those tasks are dispatched.
                Configurable properties include rate
                limits, retry options, target types, and
                others.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudtasks.GetQueueRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_queue,
            default_retry=retries.AsyncRetry(
                initial=0.1,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=20.0,
            ),
            default_timeout=20.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_queue(
        self,
        request: Optional[Union[cloudtasks.CreateQueueRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        queue: Optional[gct_queue.Queue] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gct_queue.Queue:
        r"""Creates a queue.

        Queues created with this method allow tasks to live for a
        maximum of 31 days. After a task is 31 days old, the task will
        be deleted regardless of whether it was dispatched or not.

        WARNING: Using this method may have unintended side effects if
        you are using an App Engine ``queue.yaml`` or ``queue.xml`` file
        to manage your queues. Read `Overview of Queue Management and
        queue.yaml <https://cloud.google.com/tasks/docs/queue-yaml>`__
        before using this method.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import tasks_v2beta2

            async def sample_create_queue():
                # Create a client
                client = tasks_v2beta2.CloudTasksAsyncClient()

                # Initialize request argument(s)
                request = tasks_v2beta2.CreateQueueRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.create_queue(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.tasks_v2beta2.types.CreateQueueRequest, dict]]):
                The request object. Request message for
                [CreateQueue][google.cloud.tasks.v2beta2.CloudTasks.CreateQueue].
            parent (:class:`str`):
                Required. The location name in which the queue will be
                created. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID``

                The list of allowed locations can be obtained by calling
                Cloud Tasks' implementation of
                [ListLocations][google.cloud.location.Locations.ListLocations].

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            queue (:class:`google.cloud.tasks_v2beta2.types.Queue`):
                Required. The queue to create.

                [Queue's name][google.cloud.tasks.v2beta2.Queue.name]
                cannot be the same as an existing queue.

                This corresponds to the ``queue`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tasks_v2beta2.types.Queue:
                A queue is a container of related
                tasks. Queues are configured to manage
                how those tasks are dispatched.
                Configurable properties include rate
                limits, retry options, target types, and
                others.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, queue])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudtasks.CreateQueueRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if queue is not None:
            request.queue = queue

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_queue,
            default_timeout=20.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_queue(
        self,
        request: Optional[Union[cloudtasks.UpdateQueueRequest, dict]] = None,
        *,
        queue: Optional[gct_queue.Queue] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gct_queue.Queue:
        r"""Updates a queue.

        This method creates the queue if it does not exist and updates
        the queue if it does exist.

        Queues created with this method allow tasks to live for a
        maximum of 31 days. After a task is 31 days old, the task will
        be deleted regardless of whether it was dispatched or not.

        WARNING: Using this method may have unintended side effects if
        you are using an App Engine ``queue.yaml`` or ``queue.xml`` file
        to manage your queues. Read `Overview of Queue Management and
        queue.yaml <https://cloud.google.com/tasks/docs/queue-yaml>`__
        before using this method.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import tasks_v2beta2

            async def sample_update_queue():
                # Create a client
                client = tasks_v2beta2.CloudTasksAsyncClient()

                # Initialize request argument(s)
                request = tasks_v2beta2.UpdateQueueRequest(
                )

                # Make the request
                response = await client.update_queue(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.tasks_v2beta2.types.UpdateQueueRequest, dict]]):
                The request object. Request message for
                [UpdateQueue][google.cloud.tasks.v2beta2.CloudTasks.UpdateQueue].
            queue (:class:`google.cloud.tasks_v2beta2.types.Queue`):
                Required. The queue to create or update.

                The queue's
                [name][google.cloud.tasks.v2beta2.Queue.name] must be
                specified.

                Output only fields cannot be modified using UpdateQueue.
                Any value specified for an output only field will be
                ignored. The queue's
                [name][google.cloud.tasks.v2beta2.Queue.name] cannot be
                changed.

                This corresponds to the ``queue`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                A mask used to specify which fields
                of the queue are being updated.
                If empty, then all fields will be
                updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tasks_v2beta2.types.Queue:
                A queue is a container of related
                tasks. Queues are configured to manage
                how those tasks are dispatched.
                Configurable properties include rate
                limits, retry options, target types, and
                others.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([queue, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudtasks.UpdateQueueRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if queue is not None:
            request.queue = queue
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_queue,
            default_timeout=20.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("queue.name", request.queue.name),)
            ),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_queue(
        self,
        request: Optional[Union[cloudtasks.DeleteQueueRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a queue.

        This command will delete the queue even if it has tasks in it.

        Note: If you delete a queue, a queue with the same name can't be
        created for 7 days.

        WARNING: Using this method may have unintended side effects if
        you are using an App Engine ``queue.yaml`` or ``queue.xml`` file
        to manage your queues. Read `Overview of Queue Management and
        queue.yaml <https://cloud.google.com/tasks/docs/queue-yaml>`__
        before using this method.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import tasks_v2beta2

            async def sample_delete_queue():
                # Create a client
                client = tasks_v2beta2.CloudTasksAsyncClient()

                # Initialize request argument(s)
                request = tasks_v2beta2.DeleteQueueRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_queue(request=request)

        Args:
            request (Optional[Union[google.cloud.tasks_v2beta2.types.DeleteQueueRequest, dict]]):
                The request object. Request message for
                [DeleteQueue][google.cloud.tasks.v2beta2.CloudTasks.DeleteQueue].
            name (:class:`str`):
                Required. The queue name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudtasks.DeleteQueueRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_queue,
            default_retry=retries.AsyncRetry(
                initial=0.1,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=20.0,
            ),
            default_timeout=20.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def purge_queue(
        self,
        request: Optional[Union[cloudtasks.PurgeQueueRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> queue.Queue:
        r"""Purges a queue by deleting all of its tasks.

        All tasks created before this method is called are
        permanently deleted.

        Purge operations can take up to one minute to take
        effect. Tasks might be dispatched before the purge takes
        effect. A purge is irreversible.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import tasks_v2beta2

            async def sample_purge_queue():
                # Create a client
                client = tasks_v2beta2.CloudTasksAsyncClient()

                # Initialize request argument(s)
                request = tasks_v2beta2.PurgeQueueRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.purge_queue(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.tasks_v2beta2.types.PurgeQueueRequest, dict]]):
                The request object. Request message for
                [PurgeQueue][google.cloud.tasks.v2beta2.CloudTasks.PurgeQueue].
            name (:class:`str`):
                Required. The queue name. For example:
                ``projects/PROJECT_ID/location/LOCATION_ID/queues/QUEUE_ID``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tasks_v2beta2.types.Queue:
                A queue is a container of related
                tasks. Queues are configured to manage
                how those tasks are dispatched.
                Configurable properties include rate
                limits, retry options, target types, and
                others.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudtasks.PurgeQueueRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.purge_queue,
            default_timeout=20.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def pause_queue(
        self,
        request: Optional[Union[cloudtasks.PauseQueueRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> queue.Queue:
        r"""Pauses the queue.

        If a queue is paused then the system will stop dispatching tasks
        until the queue is resumed via
        [ResumeQueue][google.cloud.tasks.v2beta2.CloudTasks.ResumeQueue].
        Tasks can still be added when the queue is paused. A queue is
        paused if its [state][google.cloud.tasks.v2beta2.Queue.state] is
        [PAUSED][google.cloud.tasks.v2beta2.Queue.State.PAUSED].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import tasks_v2beta2

            async def sample_pause_queue():
                # Create a client
                client = tasks_v2beta2.CloudTasksAsyncClient()

                # Initialize request argument(s)
                request = tasks_v2beta2.PauseQueueRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.pause_queue(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.tasks_v2beta2.types.PauseQueueRequest, dict]]):
                The request object. Request message for
                [PauseQueue][google.cloud.tasks.v2beta2.CloudTasks.PauseQueue].
            name (:class:`str`):
                Required. The queue name. For example:
                ``projects/PROJECT_ID/location/LOCATION_ID/queues/QUEUE_ID``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tasks_v2beta2.types.Queue:
                A queue is a container of related
                tasks. Queues are configured to manage
                how those tasks are dispatched.
                Configurable properties include rate
                limits, retry options, target types, and
                others.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudtasks.PauseQueueRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.pause_queue,
            default_timeout=20.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def resume_queue(
        self,
        request: Optional[Union[cloudtasks.ResumeQueueRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> queue.Queue:
        r"""Resume a queue.

        This method resumes a queue after it has been
        [PAUSED][google.cloud.tasks.v2beta2.Queue.State.PAUSED] or
        [DISABLED][google.cloud.tasks.v2beta2.Queue.State.DISABLED]. The
        state of a queue is stored in the queue's
        [state][google.cloud.tasks.v2beta2.Queue.state]; after calling
        this method it will be set to
        [RUNNING][google.cloud.tasks.v2beta2.Queue.State.RUNNING].

        WARNING: Resuming many high-QPS queues at the same time can lead
        to target overloading. If you are resuming high-QPS queues,
        follow the 500/50/5 pattern described in `Managing Cloud Tasks
        Scaling
        Risks <https://cloud.google.com/tasks/docs/manage-cloud-task-scaling>`__.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import tasks_v2beta2

            async def sample_resume_queue():
                # Create a client
                client = tasks_v2beta2.CloudTasksAsyncClient()

                # Initialize request argument(s)
                request = tasks_v2beta2.ResumeQueueRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.resume_queue(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.tasks_v2beta2.types.ResumeQueueRequest, dict]]):
                The request object. Request message for
                [ResumeQueue][google.cloud.tasks.v2beta2.CloudTasks.ResumeQueue].
            name (:class:`str`):
                Required. The queue name. For example:
                ``projects/PROJECT_ID/location/LOCATION_ID/queues/QUEUE_ID``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tasks_v2beta2.types.Queue:
                A queue is a container of related
                tasks. Queues are configured to manage
                how those tasks are dispatched.
                Configurable properties include rate
                limits, retry options, target types, and
                others.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudtasks.ResumeQueueRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.resume_queue,
            default_timeout=20.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def upload_queue_yaml(
        self,
        request: Optional[Union[cloudtasks.UploadQueueYamlRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Update queue list by uploading a queue.yaml file.

        The queue.yaml file is supplied in the request body as a
        YAML encoded string. This method was added to support
        gcloud clients versions before 322.0.0. New clients
        should use CreateQueue instead of this method.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import tasks_v2beta2

            async def sample_upload_queue_yaml():
                # Create a client
                client = tasks_v2beta2.CloudTasksAsyncClient()

                # Initialize request argument(s)
                request = tasks_v2beta2.UploadQueueYamlRequest(
                    app_id="app_id_value",
                )

                # Make the request
                await client.upload_queue_yaml(request=request)

        Args:
            request (Optional[Union[google.cloud.tasks_v2beta2.types.UploadQueueYamlRequest, dict]]):
                The request object. Request message for
                [UploadQueueYaml][google.cloud.tasks.v2beta2.CloudTasks.UploadQueueYaml].
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        request = cloudtasks.UploadQueueYamlRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.upload_queue_yaml,
            default_timeout=20.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def get_iam_policy(
        self,
        request: Optional[Union[iam_policy_pb2.GetIamPolicyRequest, dict]] = None,
        *,
        resource: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Gets the access control policy for a
        [Queue][google.cloud.tasks.v2beta2.Queue]. Returns an empty
        policy if the resource exists and does not have a policy set.

        Authorization requires the following `Google
        IAM <https://cloud.google.com/iam>`__ permission on the
        specified resource parent:

        -  ``cloudtasks.queues.getIamPolicy``

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import tasks_v2beta2
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            async def sample_get_iam_policy():
                # Create a client
                client = tasks_v2beta2.CloudTasksAsyncClient()

                # Initialize request argument(s)
                request = iam_policy_pb2.GetIamPolicyRequest(
                    resource="resource_value",
                )

                # Make the request
                response = await client.get_iam_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.iam.v1.iam_policy_pb2.GetIamPolicyRequest, dict]]):
                The request object. Request message for ``GetIamPolicy`` method.
            resource (:class:`str`):
                REQUIRED: The resource for which the
                policy is being requested. See the
                operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.policy_pb2.Policy:
                An Identity and Access Management (IAM) policy, which specifies access
                   controls for Google Cloud resources.

                   A Policy is a collection of bindings. A binding binds
                   one or more members, or principals, to a single role.
                   Principals can be user accounts, service accounts,
                   Google groups, and domains (such as G Suite). A role
                   is a named list of permissions; each role can be an
                   IAM predefined role or a user-created custom role.

                   For some types of Google Cloud resources, a binding
                   can also specify a condition, which is a logical
                   expression that allows access to a resource only if
                   the expression evaluates to true. A condition can add
                   constraints based on attributes of the request, the
                   resource, or both. To learn which resources support
                   conditions in their IAM policies, see the [IAM
                   documentation](\ https://cloud.google.com/iam/help/conditions/resource-policies).

                   **JSON example:**

                   :literal:`\`     {       "bindings": [         {           "role": "roles/resourcemanager.organizationAdmin",           "members": [             "user:mike@example.com",             "group:admins@example.com",             "domain:google.com",             "serviceAccount:my-project-id@appspot.gserviceaccount.com"           ]         },         {           "role": "roles/resourcemanager.organizationViewer",           "members": [             "user:eve@example.com"           ],           "condition": {             "title": "expirable access",             "description": "Does not grant access after Sep 2020",             "expression": "request.time <             timestamp('2020-10-01T00:00:00.000Z')",           }         }       ],       "etag": "BwWWja0YfJA=",       "version": 3     }`\ \`

                   **YAML example:**

                   :literal:`\`     bindings:     - members:       - user:mike@example.com       - group:admins@example.com       - domain:google.com       - serviceAccount:my-project-id@appspot.gserviceaccount.com       role: roles/resourcemanager.organizationAdmin     - members:       - user:eve@example.com       role: roles/resourcemanager.organizationViewer       condition:         title: expirable access         description: Does not grant access after Sep 2020         expression: request.time < timestamp('2020-10-01T00:00:00.000Z')     etag: BwWWja0YfJA=     version: 3`\ \`

                   For a description of IAM and its features, see the
                   [IAM
                   documentation](\ https://cloud.google.com/iam/docs/).

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.GetIamPolicyRequest(**request)
        elif not request:
            request = iam_policy_pb2.GetIamPolicyRequest(
                resource=resource,
            )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_iam_policy,
            default_retry=retries.AsyncRetry(
                initial=0.1,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=20.0,
            ),
            default_timeout=20.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def set_iam_policy(
        self,
        request: Optional[Union[iam_policy_pb2.SetIamPolicyRequest, dict]] = None,
        *,
        resource: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Sets the access control policy for a
        [Queue][google.cloud.tasks.v2beta2.Queue]. Replaces any existing
        policy.

        Note: The Cloud Console does not check queue-level IAM
        permissions yet. Project-level permissions are required to use
        the Cloud Console.

        Authorization requires the following `Google
        IAM <https://cloud.google.com/iam>`__ permission on the
        specified resource parent:

        -  ``cloudtasks.queues.setIamPolicy``

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import tasks_v2beta2
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            async def sample_set_iam_policy():
                # Create a client
                client = tasks_v2beta2.CloudTasksAsyncClient()

                # Initialize request argument(s)
                request = iam_policy_pb2.SetIamPolicyRequest(
                    resource="resource_value",
                )

                # Make the request
                response = await client.set_iam_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.iam.v1.iam_policy_pb2.SetIamPolicyRequest, dict]]):
                The request object. Request message for ``SetIamPolicy`` method.
            resource (:class:`str`):
                REQUIRED: The resource for which the
                policy is being specified. See the
                operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.policy_pb2.Policy:
                An Identity and Access Management (IAM) policy, which specifies access
                   controls for Google Cloud resources.

                   A Policy is a collection of bindings. A binding binds
                   one or more members, or principals, to a single role.
                   Principals can be user accounts, service accounts,
                   Google groups, and domains (such as G Suite). A role
                   is a named list of permissions; each role can be an
                   IAM predefined role or a user-created custom role.

                   For some types of Google Cloud resources, a binding
                   can also specify a condition, which is a logical
                   expression that allows access to a resource only if
                   the expression evaluates to true. A condition can add
                   constraints based on attributes of the request, the
                   resource, or both. To learn which resources support
                   conditions in their IAM policies, see the [IAM
                   documentation](\ https://cloud.google.com/iam/help/conditions/resource-policies).

                   **JSON example:**

                   :literal:`\`     {       "bindings": [         {           "role": "roles/resourcemanager.organizationAdmin",           "members": [             "user:mike@example.com",             "group:admins@example.com",             "domain:google.com",             "serviceAccount:my-project-id@appspot.gserviceaccount.com"           ]         },         {           "role": "roles/resourcemanager.organizationViewer",           "members": [             "user:eve@example.com"           ],           "condition": {             "title": "expirable access",             "description": "Does not grant access after Sep 2020",             "expression": "request.time <             timestamp('2020-10-01T00:00:00.000Z')",           }         }       ],       "etag": "BwWWja0YfJA=",       "version": 3     }`\ \`

                   **YAML example:**

                   :literal:`\`     bindings:     - members:       - user:mike@example.com       - group:admins@example.com       - domain:google.com       - serviceAccount:my-project-id@appspot.gserviceaccount.com       role: roles/resourcemanager.organizationAdmin     - members:       - user:eve@example.com       role: roles/resourcemanager.organizationViewer       condition:         title: expirable access         description: Does not grant access after Sep 2020         expression: request.time < timestamp('2020-10-01T00:00:00.000Z')     etag: BwWWja0YfJA=     version: 3`\ \`

                   For a description of IAM and its features, see the
                   [IAM
                   documentation](\ https://cloud.google.com/iam/docs/).

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.SetIamPolicyRequest(**request)
        elif not request:
            request = iam_policy_pb2.SetIamPolicyRequest(
                resource=resource,
            )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.set_iam_policy,
            default_timeout=20.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def test_iam_permissions(
        self,
        request: Optional[Union[iam_policy_pb2.TestIamPermissionsRequest, dict]] = None,
        *,
        resource: Optional[str] = None,
        permissions: Optional[MutableSequence[str]] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        r"""Returns permissions that a caller has on a
        [Queue][google.cloud.tasks.v2beta2.Queue]. If the resource does
        not exist, this will return an empty set of permissions, not a
        [NOT_FOUND][google.rpc.Code.NOT_FOUND] error.

        Note: This operation is designed to be used for building
        permission-aware UIs and command-line tools, not for
        authorization checking. This operation may "fail open" without
        warning.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import tasks_v2beta2
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            async def sample_test_iam_permissions():
                # Create a client
                client = tasks_v2beta2.CloudTasksAsyncClient()

                # Initialize request argument(s)
                request = iam_policy_pb2.TestIamPermissionsRequest(
                    resource="resource_value",
                    permissions=['permissions_value1', 'permissions_value2'],
                )

                # Make the request
                response = await client.test_iam_permissions(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.iam.v1.iam_policy_pb2.TestIamPermissionsRequest, dict]]):
                The request object. Request message for ``TestIamPermissions`` method.
            resource (:class:`str`):
                REQUIRED: The resource for which the
                policy detail is being requested. See
                the operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            permissions (:class:`MutableSequence[str]`):
                The set of permissions to check for the ``resource``.
                Permissions with wildcards (such as '*' or 'storage.*')
                are not allowed. For more information see `IAM
                Overview <https://cloud.google.com/iam/docs/overview#permissions>`__.

                This corresponds to the ``permissions`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.iam_policy_pb2.TestIamPermissionsResponse:
                Response message for TestIamPermissions method.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource, permissions])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.TestIamPermissionsRequest(**request)
        elif not request:
            request = iam_policy_pb2.TestIamPermissionsRequest(
                resource=resource,
                permissions=permissions,
            )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.test_iam_permissions,
            default_retry=retries.AsyncRetry(
                initial=0.1,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=20.0,
            ),
            default_timeout=20.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_tasks(
        self,
        request: Optional[Union[cloudtasks.ListTasksRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTasksAsyncPager:
        r"""Lists the tasks in a queue.

        By default, only the
        [BASIC][google.cloud.tasks.v2beta2.Task.View.BASIC] view is
        retrieved due to performance considerations;
        [response_view][google.cloud.tasks.v2beta2.ListTasksRequest.response_view]
        controls the subset of information which is returned.

        The tasks may be returned in any order. The ordering may change
        at any time.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import tasks_v2beta2

            async def sample_list_tasks():
                # Create a client
                client = tasks_v2beta2.CloudTasksAsyncClient()

                # Initialize request argument(s)
                request = tasks_v2beta2.ListTasksRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_tasks(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.tasks_v2beta2.types.ListTasksRequest, dict]]):
                The request object. Request message for listing tasks using
                [ListTasks][google.cloud.tasks.v2beta2.CloudTasks.ListTasks].
            parent (:class:`str`):
                Required. The queue name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tasks_v2beta2.services.cloud_tasks.pagers.ListTasksAsyncPager:
                Response message for listing tasks using
                   [ListTasks][google.cloud.tasks.v2beta2.CloudTasks.ListTasks].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudtasks.ListTasksRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_tasks,
            default_retry=retries.AsyncRetry(
                initial=0.1,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=20.0,
            ),
            default_timeout=20.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListTasksAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_task(
        self,
        request: Optional[Union[cloudtasks.GetTaskRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> task.Task:
        r"""Gets a task.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import tasks_v2beta2

            async def sample_get_task():
                # Create a client
                client = tasks_v2beta2.CloudTasksAsyncClient()

                # Initialize request argument(s)
                request = tasks_v2beta2.GetTaskRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_task(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.tasks_v2beta2.types.GetTaskRequest, dict]]):
                The request object. Request message for getting a task using
                [GetTask][google.cloud.tasks.v2beta2.CloudTasks.GetTask].
            name (:class:`str`):
                Required. The task name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID/tasks/TASK_ID``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tasks_v2beta2.types.Task:
                A unit of scheduled work.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudtasks.GetTaskRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_task,
            default_retry=retries.AsyncRetry(
                initial=0.1,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=20.0,
            ),
            default_timeout=20.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_task(
        self,
        request: Optional[Union[cloudtasks.CreateTaskRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        task: Optional[gct_task.Task] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gct_task.Task:
        r"""Creates a task and adds it to a queue.

        Tasks cannot be updated after creation; there is no UpdateTask
        command.

        -  For [App Engine
           queues][google.cloud.tasks.v2beta2.AppEngineHttpTarget], the
           maximum task size is 100KB.
        -  For [pull queues][google.cloud.tasks.v2beta2.PullTarget], the
           maximum task size is 1MB.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import tasks_v2beta2

            async def sample_create_task():
                # Create a client
                client = tasks_v2beta2.CloudTasksAsyncClient()

                # Initialize request argument(s)
                request = tasks_v2beta2.CreateTaskRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.create_task(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.tasks_v2beta2.types.CreateTaskRequest, dict]]):
                The request object. Request message for
                [CreateTask][google.cloud.tasks.v2beta2.CloudTasks.CreateTask].
            parent (:class:`str`):
                Required. The queue name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID``

                The queue must already exist.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            task (:class:`google.cloud.tasks_v2beta2.types.Task`):
                Required. The task to add.

                Task names have the following format:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID/tasks/TASK_ID``.
                The user can optionally specify a task
                [name][google.cloud.tasks.v2beta2.Task.name]. If a name
                is not specified then the system will generate a random
                unique task id, which will be set in the task returned
                in the [response][google.cloud.tasks.v2beta2.Task.name].

                If
                [schedule_time][google.cloud.tasks.v2beta2.Task.schedule_time]
                is not set or is in the past then Cloud Tasks will set
                it to the current time.

                Task De-duplication:

                Explicitly specifying a task ID enables task
                de-duplication. If a task's ID is identical to that of
                an existing task or a task that was deleted or completed
                recently then the call will fail with
                [ALREADY_EXISTS][google.rpc.Code.ALREADY_EXISTS]. If the
                task's queue was created using Cloud Tasks, then another
                task with the same name can't be created for ~1 hour
                after the original task was deleted or completed. If the
                task's queue was created using queue.yaml or queue.xml,
                then another task with the same name can't be created
                for ~9 days after the original task was deleted or
                completed.

                Because there is an extra lookup cost to identify
                duplicate task names, these
                [CreateTask][google.cloud.tasks.v2beta2.CloudTasks.CreateTask]
                calls have significantly increased latency. Using hashed
                strings for the task id or for the prefix of the task id
                is recommended. Choosing task ids that are sequential or
                have sequential prefixes, for example using a timestamp,
                causes an increase in latency and error rates in all
                task commands. The infrastructure relies on an
                approximately uniform distribution of task ids to store
                and serve tasks efficiently.

                This corresponds to the ``task`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tasks_v2beta2.types.Task:
                A unit of scheduled work.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, task])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudtasks.CreateTaskRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if task is not None:
            request.task = task

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_task,
            default_timeout=20.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_task(
        self,
        request: Optional[Union[cloudtasks.DeleteTaskRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a task.

        A task can be deleted if it is scheduled or dispatched.
        A task cannot be deleted if it has completed
        successfully or permanently failed.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import tasks_v2beta2

            async def sample_delete_task():
                # Create a client
                client = tasks_v2beta2.CloudTasksAsyncClient()

                # Initialize request argument(s)
                request = tasks_v2beta2.DeleteTaskRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_task(request=request)

        Args:
            request (Optional[Union[google.cloud.tasks_v2beta2.types.DeleteTaskRequest, dict]]):
                The request object. Request message for deleting a task using
                [DeleteTask][google.cloud.tasks.v2beta2.CloudTasks.DeleteTask].
            name (:class:`str`):
                Required. The task name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID/tasks/TASK_ID``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudtasks.DeleteTaskRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_task,
            default_retry=retries.AsyncRetry(
                initial=0.1,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=20.0,
            ),
            default_timeout=20.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def lease_tasks(
        self,
        request: Optional[Union[cloudtasks.LeaseTasksRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        lease_duration: Optional[duration_pb2.Duration] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloudtasks.LeaseTasksResponse:
        r"""Leases tasks from a pull queue for
        [lease_duration][google.cloud.tasks.v2beta2.LeaseTasksRequest.lease_duration].

        This method is invoked by the worker to obtain a lease. The
        worker must acknowledge the task via
        [AcknowledgeTask][google.cloud.tasks.v2beta2.CloudTasks.AcknowledgeTask]
        after they have performed the work associated with the task.

        The [payload][google.cloud.tasks.v2beta2.PullMessage.payload] is
        intended to store data that the worker needs to perform the work
        associated with the task. To return the payloads in the
        [response][google.cloud.tasks.v2beta2.LeaseTasksResponse], set
        [response_view][google.cloud.tasks.v2beta2.LeaseTasksRequest.response_view]
        to [FULL][google.cloud.tasks.v2beta2.Task.View.FULL].

        A maximum of 10 qps of
        [LeaseTasks][google.cloud.tasks.v2beta2.CloudTasks.LeaseTasks]
        requests are allowed per queue.
        [RESOURCE_EXHAUSTED][google.rpc.Code.RESOURCE_EXHAUSTED] is
        returned when this limit is exceeded.
        [RESOURCE_EXHAUSTED][google.rpc.Code.RESOURCE_EXHAUSTED] is also
        returned when
        [max_tasks_dispatched_per_second][google.cloud.tasks.v2beta2.RateLimits.max_tasks_dispatched_per_second]
        is exceeded.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import tasks_v2beta2

            async def sample_lease_tasks():
                # Create a client
                client = tasks_v2beta2.CloudTasksAsyncClient()

                # Initialize request argument(s)
                request = tasks_v2beta2.LeaseTasksRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.lease_tasks(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.tasks_v2beta2.types.LeaseTasksRequest, dict]]):
                The request object. Request message for leasing tasks using
                [LeaseTasks][google.cloud.tasks.v2beta2.CloudTasks.LeaseTasks].
            parent (:class:`str`):
                Required. The queue name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            lease_duration (:class:`google.protobuf.duration_pb2.Duration`):
                Required. The duration of the lease.

                Each task returned in the
                [response][google.cloud.tasks.v2beta2.LeaseTasksResponse]
                will have its
                [schedule_time][google.cloud.tasks.v2beta2.Task.schedule_time]
                set to the current time plus the ``lease_duration``. The
                task is leased until its
                [schedule_time][google.cloud.tasks.v2beta2.Task.schedule_time];
                thus, the task will not be returned to another
                [LeaseTasks][google.cloud.tasks.v2beta2.CloudTasks.LeaseTasks]
                call before its
                [schedule_time][google.cloud.tasks.v2beta2.Task.schedule_time].

                After the worker has successfully finished the work
                associated with the task, the worker must call via
                [AcknowledgeTask][google.cloud.tasks.v2beta2.CloudTasks.AcknowledgeTask]
                before the
                [schedule_time][google.cloud.tasks.v2beta2.Task.schedule_time].
                Otherwise the task will be returned to a later
                [LeaseTasks][google.cloud.tasks.v2beta2.CloudTasks.LeaseTasks]
                call so that another worker can retry it.

                The maximum lease duration is 1 week. ``lease_duration``
                will be truncated to the nearest second.

                This corresponds to the ``lease_duration`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tasks_v2beta2.types.LeaseTasksResponse:
                Response message for leasing tasks using
                   [LeaseTasks][google.cloud.tasks.v2beta2.CloudTasks.LeaseTasks].

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, lease_duration])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudtasks.LeaseTasksRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if lease_duration is not None:
            request.lease_duration = lease_duration

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.lease_tasks,
            default_timeout=20.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def acknowledge_task(
        self,
        request: Optional[Union[cloudtasks.AcknowledgeTaskRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        schedule_time: Optional[timestamp_pb2.Timestamp] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Acknowledges a pull task.

        The worker, that is, the entity that
        [leased][google.cloud.tasks.v2beta2.CloudTasks.LeaseTasks] this
        task must call this method to indicate that the work associated
        with the task has finished.

        The worker must acknowledge a task within the
        [lease_duration][google.cloud.tasks.v2beta2.LeaseTasksRequest.lease_duration]
        or the lease will expire and the task will become available to
        be leased again. After the task is acknowledged, it will not be
        returned by a later
        [LeaseTasks][google.cloud.tasks.v2beta2.CloudTasks.LeaseTasks],
        [GetTask][google.cloud.tasks.v2beta2.CloudTasks.GetTask], or
        [ListTasks][google.cloud.tasks.v2beta2.CloudTasks.ListTasks].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import tasks_v2beta2

            async def sample_acknowledge_task():
                # Create a client
                client = tasks_v2beta2.CloudTasksAsyncClient()

                # Initialize request argument(s)
                request = tasks_v2beta2.AcknowledgeTaskRequest(
                    name="name_value",
                )

                # Make the request
                await client.acknowledge_task(request=request)

        Args:
            request (Optional[Union[google.cloud.tasks_v2beta2.types.AcknowledgeTaskRequest, dict]]):
                The request object. Request message for acknowledging a task using
                [AcknowledgeTask][google.cloud.tasks.v2beta2.CloudTasks.AcknowledgeTask].
            name (:class:`str`):
                Required. The task name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID/tasks/TASK_ID``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            schedule_time (:class:`google.protobuf.timestamp_pb2.Timestamp`):
                Required. The task's current schedule time, available in
                the
                [schedule_time][google.cloud.tasks.v2beta2.Task.schedule_time]
                returned by
                [LeaseTasks][google.cloud.tasks.v2beta2.CloudTasks.LeaseTasks]
                response or
                [RenewLease][google.cloud.tasks.v2beta2.CloudTasks.RenewLease]
                response. This restriction is to ensure that your worker
                currently holds the lease.

                This corresponds to the ``schedule_time`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, schedule_time])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudtasks.AcknowledgeTaskRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if schedule_time is not None:
            request.schedule_time = schedule_time

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.acknowledge_task,
            default_timeout=20.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def renew_lease(
        self,
        request: Optional[Union[cloudtasks.RenewLeaseRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        schedule_time: Optional[timestamp_pb2.Timestamp] = None,
        lease_duration: Optional[duration_pb2.Duration] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> task.Task:
        r"""Renew the current lease of a pull task.

        The worker can use this method to extend the lease by a new
        duration, starting from now. The new task lease will be returned
        in the task's
        [schedule_time][google.cloud.tasks.v2beta2.Task.schedule_time].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import tasks_v2beta2

            async def sample_renew_lease():
                # Create a client
                client = tasks_v2beta2.CloudTasksAsyncClient()

                # Initialize request argument(s)
                request = tasks_v2beta2.RenewLeaseRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.renew_lease(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.tasks_v2beta2.types.RenewLeaseRequest, dict]]):
                The request object. Request message for renewing a lease using
                [RenewLease][google.cloud.tasks.v2beta2.CloudTasks.RenewLease].
            name (:class:`str`):
                Required. The task name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID/tasks/TASK_ID``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            schedule_time (:class:`google.protobuf.timestamp_pb2.Timestamp`):
                Required. The task's current schedule time, available in
                the
                [schedule_time][google.cloud.tasks.v2beta2.Task.schedule_time]
                returned by
                [LeaseTasks][google.cloud.tasks.v2beta2.CloudTasks.LeaseTasks]
                response or
                [RenewLease][google.cloud.tasks.v2beta2.CloudTasks.RenewLease]
                response. This restriction is to ensure that your worker
                currently holds the lease.

                This corresponds to the ``schedule_time`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            lease_duration (:class:`google.protobuf.duration_pb2.Duration`):
                Required. The desired new lease duration, starting from
                now.

                The maximum lease duration is 1 week. ``lease_duration``
                will be truncated to the nearest second.

                This corresponds to the ``lease_duration`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tasks_v2beta2.types.Task:
                A unit of scheduled work.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, schedule_time, lease_duration])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudtasks.RenewLeaseRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if schedule_time is not None:
            request.schedule_time = schedule_time
        if lease_duration is not None:
            request.lease_duration = lease_duration

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.renew_lease,
            default_timeout=20.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def cancel_lease(
        self,
        request: Optional[Union[cloudtasks.CancelLeaseRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        schedule_time: Optional[timestamp_pb2.Timestamp] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> task.Task:
        r"""Cancel a pull task's lease.

        The worker can use this method to cancel a task's lease by
        setting its
        [schedule_time][google.cloud.tasks.v2beta2.Task.schedule_time]
        to now. This will make the task available to be leased to the
        next caller of
        [LeaseTasks][google.cloud.tasks.v2beta2.CloudTasks.LeaseTasks].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import tasks_v2beta2

            async def sample_cancel_lease():
                # Create a client
                client = tasks_v2beta2.CloudTasksAsyncClient()

                # Initialize request argument(s)
                request = tasks_v2beta2.CancelLeaseRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.cancel_lease(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.tasks_v2beta2.types.CancelLeaseRequest, dict]]):
                The request object. Request message for canceling a lease using
                [CancelLease][google.cloud.tasks.v2beta2.CloudTasks.CancelLease].
            name (:class:`str`):
                Required. The task name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID/tasks/TASK_ID``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            schedule_time (:class:`google.protobuf.timestamp_pb2.Timestamp`):
                Required. The task's current schedule time, available in
                the
                [schedule_time][google.cloud.tasks.v2beta2.Task.schedule_time]
                returned by
                [LeaseTasks][google.cloud.tasks.v2beta2.CloudTasks.LeaseTasks]
                response or
                [RenewLease][google.cloud.tasks.v2beta2.CloudTasks.RenewLease]
                response. This restriction is to ensure that your worker
                currently holds the lease.

                This corresponds to the ``schedule_time`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tasks_v2beta2.types.Task:
                A unit of scheduled work.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, schedule_time])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudtasks.CancelLeaseRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if schedule_time is not None:
            request.schedule_time = schedule_time

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.cancel_lease,
            default_timeout=20.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def run_task(
        self,
        request: Optional[Union[cloudtasks.RunTaskRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> task.Task:
        r"""Forces a task to run now.

        When this method is called, Cloud Tasks will dispatch the task,
        even if the task is already running, the queue has reached its
        [RateLimits][google.cloud.tasks.v2beta2.RateLimits] or is
        [PAUSED][google.cloud.tasks.v2beta2.Queue.State.PAUSED].

        This command is meant to be used for manual debugging. For
        example,
        [RunTask][google.cloud.tasks.v2beta2.CloudTasks.RunTask] can be
        used to retry a failed task after a fix has been made or to
        manually force a task to be dispatched now.

        The dispatched task is returned. That is, the task that is
        returned contains the
        [status][google.cloud.tasks.v2beta2.Task.status] after the task
        is dispatched but before the task is received by its target.

        If Cloud Tasks receives a successful response from the task's
        target, then the task will be deleted; otherwise the task's
        [schedule_time][google.cloud.tasks.v2beta2.Task.schedule_time]
        will be reset to the time that
        [RunTask][google.cloud.tasks.v2beta2.CloudTasks.RunTask] was
        called plus the retry delay specified in the queue's
        [RetryConfig][google.cloud.tasks.v2beta2.RetryConfig].

        [RunTask][google.cloud.tasks.v2beta2.CloudTasks.RunTask] returns
        [NOT_FOUND][google.rpc.Code.NOT_FOUND] when it is called on a
        task that has already succeeded or permanently failed.

        [RunTask][google.cloud.tasks.v2beta2.CloudTasks.RunTask] cannot
        be called on a [pull
        task][google.cloud.tasks.v2beta2.PullMessage].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import tasks_v2beta2

            async def sample_run_task():
                # Create a client
                client = tasks_v2beta2.CloudTasksAsyncClient()

                # Initialize request argument(s)
                request = tasks_v2beta2.RunTaskRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.run_task(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.tasks_v2beta2.types.RunTaskRequest, dict]]):
                The request object. Request message for forcing a task to run now using
                [RunTask][google.cloud.tasks.v2beta2.CloudTasks.RunTask].
            name (:class:`str`):
                Required. The task name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID/tasks/TASK_ID``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tasks_v2beta2.types.Task:
                A unit of scheduled work.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloudtasks.RunTaskRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.run_task,
            default_timeout=20.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_location(
        self,
        request: Optional[locations_pb2.GetLocationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> locations_pb2.Location:
        r"""Gets information about a location.

        Args:
            request (:class:`~.location_pb2.GetLocationRequest`):
                The request object. Request message for
                `GetLocation` method.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors,
                 if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.location_pb2.Location:
                Location object.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = locations_pb2.GetLocationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_location,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_locations(
        self,
        request: Optional[locations_pb2.ListLocationsRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> locations_pb2.ListLocationsResponse:
        r"""Lists information about the supported locations for this service.

        Args:
            request (:class:`~.location_pb2.ListLocationsRequest`):
                The request object. Request message for
                `ListLocations` method.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors,
                 if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.location_pb2.ListLocationsResponse:
                Response message for ``ListLocations`` method.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = locations_pb2.ListLocationsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_locations,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self) -> "CloudTasksAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("CloudTasksAsyncClient",)
