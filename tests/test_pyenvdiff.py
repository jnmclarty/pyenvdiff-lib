#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pyenvdiff
----------------------------------

Tests for `pyenvdiff` module.
"""

import mock
import pytest as pt
import inspect
import sys
import os

import pyenvdiff
from pyenvdiff.collectors import Collector, collector_classes, \
    invasive_collector_classes, harmless_collector_classes
from pyenvdiff.environment import Environment, EnvironmentDiff
from pyenvdiff.arg_parsing import get_available_parser_name_and_class
from pyenvdiff.client import Client
from pyenvdiff.compat import supported_info_types
from pyenvdiff.public_post import PublicClient

mock_supported_info_instances = []

try:
    mock_supported_info_instances.append(False)
except:
    pass

try:
    mock_supported_info_instances.append(-555)
except:
    pass

try:
    mock_supported_info_instances.append(str("Non Matching"))
except:
    pass

try:
    mock_supported_info_instances.append(unicode("Non Matching"))
except:
    pass

try:
    mock_supported_info_instances.append(["a", "b", "c"])
except:
    pass

try:
    mock_supported_info_instances.append({"a" : "A", "b" : "B"})
except:
    pass

class PythonVersion(object):
    def __init__(self):
        pass
    def __getitem__(self, key):
        parts = list(map(int, key.split('.')))
        for i, version_part in enumerate(parts):
            if version_part != sys.version_info[i]:
                return False
        return True

python_version = PythonVersion()

orig_import = __import__

if python_version['2']:
    builtin = '__builtin__.__import__'
else:
    builtin = 'builtins.__import__'

class TestCollectors(object):
    def test_all_collectors_are_captured(self):
        discovered = []
        for obj_name in dir(pyenvdiff.collectors):
            obj = getattr(pyenvdiff.collectors, obj_name)
            if inspect.isclass(obj):
                if issubclass(obj, Collector) and obj is not Collector:
                    discovered.append(obj)
        assert(set(collector_classes) == set(discovered)), "All Collectors should be included in the collector_class list"
    @pt.mark.parametrize("CollectorClass", collector_classes)
    def test_equality_check(self, CollectorClass):
        assert(CollectorClass() == CollectorClass()), "Collector should be able to be compared for equality"
    @pt.mark.parametrize("CollectorClass", collector_classes)
    def test_string_returns_a_string(self, CollectorClass):
        col = str(CollectorClass())
        assert(isinstance(col, str)), "Collector should serialize to a string"
    @pt.mark.parametrize("CollectorClass", collector_classes)
    def test_english_property_exists(self, CollectorClass):
        col = CollectorClass()
        english = col.english
        assert(isinstance(english, str)), "Collector should have an english property"

class TestEnvironment(object):
    @classmethod
    def setup_class(cls):
        cls.env = Environment()

    def test_environment_init(self):
        assert isinstance(self.env, Environment)

    def test_environment_info(self):
        env_info = self.env.info()
        info_keys = [c.__name__ for c in harmless_collector_classes]
        assert set(env_info.keys()).issubset(info_keys)

    def test_environment_str(self):
        env_as_str = str(self.env)
        assert isinstance(env_as_str, str)

    def test_environment_keys(self):
        env_keys = list(self.env.collectors.keys())
        col_cls_names = [c.__name__ for c in harmless_collector_classes]
        assert set(col_cls_names).issubset(env_keys)
        assert len(col_cls_names) == len(env_keys)

    def test_environment_strs(self):
        env_keys = list(self.env.collectors.keys())
        for env_key in env_keys:
            assert len(str(self.env.collectors[env_key])) > 1

    @classmethod
    def teardown_class(cls):
        pass

class TestEnvironments(object):
    def test_identical_environments_match(self):
        env1 = Environment()
        env2 = Environment()
        ed = EnvironmentDiff(env1, env2)
        assert ed.as_bool(), "Two identical calls, should compare to true!"

    def test_identical_environments_convert_to_strings_for_every_collector(self):
        env1 = Environment()
        env2 = Environment()

        for Collector in invasive_collector_classes:
            env1 = env1 + Collector()
            env2 = env2 + Collector()

        ed = EnvironmentDiff(env1, env2)
        assert str(ed).count("MATCHING") == len(collector_classes), "Every collector should match, even erroneous one"

    @pt.mark.parametrize("CollectorClass", collector_classes)
    def test_non_matching_collectors(self, CollectorClass):
        env1 = Environment()
        env2 = Environment()

        if CollectorClass in invasive_collector_classes:
            env1 += CollectorClass()
            env2 += CollectorClass()

        actual_collector_type = type(env1.collectors[CollectorClass.__name__].info)

        type_map = dict(zip(supported_info_types, mock_supported_info_instances))

        non_matching_info = type_map.get(actual_collector_type, None)

        if non_matching_info is None:
            msg = "Every possible type of info should be handled, %s of %s is not."
            raise Exception(msg  % (actual_collector_type, CollectorClass))

        non_matching_collector = CollectorClass(non_matching_info)
        env1.collectors[CollectorClass.__name__] = non_matching_collector

        assert not EnvironmentDiff(env1, env2).as_bool()
    def test_reading_and_writing_to_yaml(self):

        if python_version['2']:
            from StringIO import StringIO
        else:
            from io import StringIO

        env1 = Environment()

        env_1_fs = StringIO()
        env_2_fs = StringIO()

        env1._to_json_fs(env_1_fs)
        env_1_fs.seek(0)
        env2 = Environment._from_json_fs(env_1_fs)
        env2._to_json_fs(env_2_fs)
        env_2_fs.seek(0)
        env3 = Environment._from_json_fs(env_2_fs)

        msg = "Reinstantiated Environments should match!"

        ed = EnvironmentDiff(env1, env3)

        print(ed)

        result = ed.as_bool()
        assert result, msg
    def test_non_matching_environment_serialization(self):
        env_a = Environment.from_file(__file__.replace("test_pyenvdiff.py", "a.json"))
        env_b = Environment.from_file(__file__.replace("test_pyenvdiff.py", "b.json"))
        ed = EnvironmentDiff(env_a, env_b)
        out = ed.for_json()
        assert type(str(ed)) is str
        assert len(out.keys()) == len(harmless_collector_classes)
        assert set(out['SysPath'].keys()).issuperset(set(['comparison', 'left', 'matching', 'right']))
        assert not out['SysPath']['matching'], "Based on the two files, these shouldn't match"
        assert out['SysPlatform']['matching'], "Based on the two files, these should match"

class TestPost(object):
    @classmethod
    def setup_class(cls):
        cls.env = Environment()


    def test_get_available_parser_name_and_class(self):
        parser_name, Parser = get_available_parser_name_and_class()
        assert parser_name in ('argparse', 'optparse', 'getopt')


    """ TODO: Figure out how to properly test this
    def test_execute_parsing_engine(self):
        parser_details = get_available_parser_name_and_class()
        args = execute_parsing_engine(*parser_details)
        print(args)
    """


    def test_getting_optparse(self):
        def import_mock(name, *args):
            if name == 'argparse':
                raise ImportError("Argparse not found")
            return orig_import(name, *args)

        with mock.patch(builtin, side_effect=import_mock):
            name, Cls = get_available_parser_name_and_class()
            assert name == 'optparse'


    def test_getting_getopt(self):
        def import_mock(name, *args):
            if name in ('optparse', 'argparse'):
                raise ImportError("Latest parsers not found")
            return orig_import(name, *args)

        with mock.patch(builtin, side_effect=import_mock):
            name, Cls = get_available_parser_name_and_class()
            assert name == 'getopt'


    @mock.patch('pyenvdiff.client.Request')
    @mock.patch('pyenvdiff.client.urlopen')
    def test_send_basic(self, urlopen, Request):

        class FakeFileStream(object):
            def read(self):
                data = '{"result" : "OK", "sha" : "123", "message" : "Good to Go!" }'
                if python_version['3']:
                    return data.encode('utf-8')
                return data

            def close(self):
                return True

        Request.return_value = True
        urlopen.return_value = FakeFileStream()

        client = Client(server='LOCAL')
        msg = client.send(self.env)
        assert "Good to Go!" in msg


    def test_get_api_key_unset(self):
        client = Client(server='LOCAL')
        with mock.patch.dict(os.environ, {}):
            assert client.api_key == Client.DEFAULT_API_KEY


    @pt.mark.parametrize("pyenvapikey_envvar,expected_apikey", [
        ('DEFAULT', Client.DEFAULT_API_KEY),
        ('123', '123')
    ])
    def test_get_api_key(self, pyenvapikey_envvar, expected_apikey):
        with mock.patch.dict(os.environ, {'PYENVDIFF_API_KEY': pyenvapikey_envvar}):
            client = Client(server='LOCAL')
            assert client.api_key == expected_apikey


    def test_get_server_url_unset(self):
        with mock.patch.dict(os.environ, {}):
            with pt.raises(Exception) as exec_info:
                Client()
            assert "Must specify a server.  Found None." in str(exec_info.value)


    @pt.mark.parametrize("pyenvserver_envvar,expected_server", [
        ('DEFAULT', 'https://osa.pyenvdiff.com'),
        ('LOCAL', Client.LOCAL_SERVER),
        ('someserver', 'someserver')])
    def test_get_server_url(self, pyenvserver_envvar, expected_server):
        with mock.patch.dict(os.environ, {'PYENVDIFF_SERVER': pyenvserver_envvar}):
            client = PublicClient()
            assert client.server == expected_server
