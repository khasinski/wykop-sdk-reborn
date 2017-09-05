from types import GeneratorType
import mock

from wykop.api.v2.clients import WykopAPIv2


class TestWykopAPIv2GetApiParams(object):

    def test_empty(self, wykop_api_v2):
        api_params = {}

        result = wykop_api_v2.get_api_params(**api_params)

        assert type(result) == GeneratorType
        assert tuple(result) == (
            'appkey', 'sentinel.appkey',
            'format', 'sentinel.format',
            'output', 'sentinel.output',
        )

    def test_none_not_mapped(self, wykop_api_v2):
        api_params = {'test1': None}
        result = wykop_api_v2.get_api_params(**api_params)

        assert type(result) == GeneratorType
        assert tuple(result) == (
            'appkey', 'sentinel.appkey',
            'format', 'sentinel.format',
            'output', 'sentinel.output',
        )

    def test_mapped(self, wykop_api_v2):
        api_params = {'test1': 1}
        result = wykop_api_v2.get_api_params(**api_params)

        assert type(result) == GeneratorType
        assert tuple(result) == (
            'test1', '1',
            'appkey', 'sentinel.appkey',
            'format', 'sentinel.format',
            'output', 'sentinel.output',
        )


class TestWykopAPIv2GetPath(object):

    @mock.patch.object(WykopAPIv2, 'get_default_api_params')
    def test_no_params(self, m_get_default_api_params, wykop_api_v2):
        m_get_default_api_params.return_value = {}
        request_type = 'request_type'

        result = wykop_api_v2.get_path(request_type)

        assert result == request_type

    @mock.patch.object(WykopAPIv2, 'get_default_api_params')
    def test_method(self, m_get_default_api_params, wykop_api_v2):
        m_get_default_api_params.return_value = {}
        request_type = 'request_type'
        request_method = 'request_method'

        result = wykop_api_v2.get_path(request_type, request_method)

        assert result == '{0}/{1}'.format(request_type, request_method)

    @mock.patch.object(WykopAPIv2, 'get_default_api_params')
    def test_api_params(self, m_get_default_api_params, wykop_api_v2):
        m_get_default_api_params.return_value = {}
        request_type = 'request_type'
        api_param_key = 'test1'
        api_param_value = 1
        api_params = {
            api_param_key: api_param_value,
        }

        result = wykop_api_v2.get_path(request_type, **api_params)

        assert result == '{0}/test1/1'.format(
            request_type, api_param_key, api_param_value,
        )


class TestWykopAPIv2ConstructUrl(object):

    @mock.patch.object(WykopAPIv2, 'get_path')
    def test_no_params(self, mocked_get_path, wykop_api_v2):
        request_type = 'request_type'
        path = 'some_path'
        mocked_get_path.return_value = path

        result = wykop_api_v2.construct_url(request_type)

        mocked_get_path.assert_called_once_with(
            request_type, rmethod=None)
        assert result == '{0}://{1}/{2}'.format(
            wykop_api_v2._protocol,
            wykop_api_v2._domain,
            path,
        )

    @mock.patch.object(WykopAPIv2, 'get_path')
    def test_request_method(self, mocked_get_path, wykop_api_v2):
        request_type = 'request_type'
        request_method = 'request_method'
        path = 'some_path'
        mocked_get_path.return_value = path

        result = wykop_api_v2.construct_url(request_type, request_method)

        mocked_get_path.assert_called_once_with(
            request_type, rmethod=request_method)
        assert result == '{0}://{1}/{2}'.format(
            wykop_api_v2._protocol,
            wykop_api_v2._domain,
            path,
        )

    @mock.patch.object(WykopAPIv2, 'get_path')
    def test_api_params(self, mocked_get_path, wykop_api_v2):
        request_type = 'request_type'
        api_param1_value = 'param1_value'
        api_param2_value = 'param2_value'
        path = 'some_path'
        mocked_get_path.return_value = path

        result = wykop_api_v2.construct_url(
            request_type,
            api_param1_name=api_param1_value,
            api_param2_name=api_param2_value,
        )

        mocked_get_path.assert_called_once_with(
            request_type,
            rmethod=None,
            api_param1_name=api_param1_value,
            api_param2_name=api_param2_value,
        )
        assert result == '{0}://{1}/{2}'.format(
            wykop_api_v2._protocol,
            wykop_api_v2._domain,
            path,
        )
