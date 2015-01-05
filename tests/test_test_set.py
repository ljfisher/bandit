# -*- coding:utf-8 -*-
#
# Copyright 2015 Nebula, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import mock
import os
import unittest

from bandit.core.test_set import BanditTestSet


class BanditTestSetTests(unittest.TestCase):

    def setUp(self):
        super(BanditTestSetTests, self).setUp()

    def tearDown(self):
        pass

    def test_register_setup_finish_funcs(self):
        test_plugins_path = os.path.join(os.getcwd(), 'tests', 'plugins')

        def get_setting(key):
            conf = {
                'plugins_dir': test_plugins_path,
                'plugin_name_pattern': '*.py',
            }
            return conf[key]

        with mock.patch('bandit.core.config.BanditConfig') as config_mock:
            config_mock.get_setting = get_setting

            test_set = BanditTestSet(logging.getLogger(), config_mock)

            self.assertEqual(
                test_set._setup_funcs[0].__name__, 'test_plugin_setup')
            self.assertEqual(
                test_set._finish_funcs[0].__name__, 'test_plugin_finish')
