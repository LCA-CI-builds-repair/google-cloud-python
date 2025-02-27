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
from typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Iterator,
    Optional,
    Sequence,
    Tuple,
)

from google.cloud.cloudquotas_v1.types import cloudquotas, resources


class ListQuotaInfosPager:
    """A pager for iterating through ``list_quota_infos`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.cloudquotas_v1.types.ListQuotaInfosResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``quota_infos`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListQuotaInfos`` requests and continue to iterate
    through the ``quota_infos`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.cloudquotas_v1.types.ListQuotaInfosResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., cloudquotas.ListQuotaInfosResponse],
        request: cloudquotas.ListQuotaInfosRequest,
        response: cloudquotas.ListQuotaInfosResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.cloudquotas_v1.types.ListQuotaInfosRequest):
                The initial request object.
            response (google.cloud.cloudquotas_v1.types.ListQuotaInfosResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = cloudquotas.ListQuotaInfosRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[cloudquotas.ListQuotaInfosResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[resources.QuotaInfo]:
        for page in self.pages:
            yield from page.quota_infos

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListQuotaInfosAsyncPager:
    """A pager for iterating through ``list_quota_infos`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.cloudquotas_v1.types.ListQuotaInfosResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``quota_infos`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListQuotaInfos`` requests and continue to iterate
    through the ``quota_infos`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.cloudquotas_v1.types.ListQuotaInfosResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[cloudquotas.ListQuotaInfosResponse]],
        request: cloudquotas.ListQuotaInfosRequest,
        response: cloudquotas.ListQuotaInfosResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.cloudquotas_v1.types.ListQuotaInfosRequest):
                The initial request object.
            response (google.cloud.cloudquotas_v1.types.ListQuotaInfosResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = cloudquotas.ListQuotaInfosRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[cloudquotas.ListQuotaInfosResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[resources.QuotaInfo]:
        async def async_generator():
            async for page in self.pages:
                for response in page.quota_infos:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListQuotaPreferencesPager:
    """A pager for iterating through ``list_quota_preferences`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.cloudquotas_v1.types.ListQuotaPreferencesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``quota_preferences`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListQuotaPreferences`` requests and continue to iterate
    through the ``quota_preferences`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.cloudquotas_v1.types.ListQuotaPreferencesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., cloudquotas.ListQuotaPreferencesResponse],
        request: cloudquotas.ListQuotaPreferencesRequest,
        response: cloudquotas.ListQuotaPreferencesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.cloudquotas_v1.types.ListQuotaPreferencesRequest):
                The initial request object.
            response (google.cloud.cloudquotas_v1.types.ListQuotaPreferencesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = cloudquotas.ListQuotaPreferencesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[cloudquotas.ListQuotaPreferencesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[resources.QuotaPreference]:
        for page in self.pages:
            yield from page.quota_preferences

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListQuotaPreferencesAsyncPager:
    """A pager for iterating through ``list_quota_preferences`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.cloudquotas_v1.types.ListQuotaPreferencesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``quota_preferences`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListQuotaPreferences`` requests and continue to iterate
    through the ``quota_preferences`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.cloudquotas_v1.types.ListQuotaPreferencesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[cloudquotas.ListQuotaPreferencesResponse]],
        request: cloudquotas.ListQuotaPreferencesRequest,
        response: cloudquotas.ListQuotaPreferencesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.cloudquotas_v1.types.ListQuotaPreferencesRequest):
                The initial request object.
            response (google.cloud.cloudquotas_v1.types.ListQuotaPreferencesResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = cloudquotas.ListQuotaPreferencesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[cloudquotas.ListQuotaPreferencesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterator[resources.QuotaPreference]:
        async def async_generator():
            async for page in self.pages:
                for response in page.quota_preferences:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
