import json
from typing import List

import pytest
import responses

import pyasq


class SimpleType:
    name: str


class ComplexType:
    stuff: List[SimpleType]


def test_basic_typing():
    with responses.RequestsMock() as rsps:
        mock_body(rsps, {'name': 'hello'})
        result = build_api(SimpleType).endpoint.get()
    assert isinstance(result, SimpleType)
    assert isinstance(result.name, str)


def test_complex_typing():
    with responses.RequestsMock() as rsps:
        mock_body(rsps, {'stuff': [{'name': 'hello'}, {'name': 'world'}]})
        result = build_api(ComplexType).endpoint.get()
    assert isinstance(result.stuff[1], SimpleType)


def test_type_validation():
    with responses.RequestsMock() as rsps:
        mock_body(rsps, {'stuff': 'banana'})
        result = build_api(ComplexType).endpoint.get()
    with pytest.raises(TypeError):
        _ = result.stuff


def test_generic_list_typing():
    class ListTypes:
        vintage: list
        modern: List

    with responses.RequestsMock() as rsps:
        mock_body(rsps, {'modern': [], 'vintage': []})
        result = build_api(ListTypes).endpoint.get()

    assert isinstance(result.modern, list)
    assert isinstance(result.vintage, list)


def test_default_values():
    class HasDefault:
        foo: str = 'hello'

    api = build_api(HasDefault)

    with responses.RequestsMock() as rsps:
        mock_body(rsps, {'foo': 'world'})
        result = api.endpoint.get()

    assert result.foo == 'world'

    with responses.RequestsMock() as rsps:
        mock_body(rsps, {})
        result = api.endpoint.get()

    assert result.foo == 'hello'


def test_type_validation():
    with responses.RequestsMock() as rsps:
        mock_body(rsps, {'name': 123})
        result = build_api(SimpleType).endpoint.get()
    with pytest.raises(TypeError):
        _ = result.name


def build_api(cls):
    @pyasq.api('http://dummy.url')
    class Api:
        @pyasq.endpoint('/endpoint')
        def endpoint(self) -> cls:
            pass
    return Api()


def mock_body(rsps, body):
    rsps.add(
        responses.GET,
        'http://dummy.url/endpoint',
        body=json.dumps(body)
    )
