# Copyright 2016 Intel Corporation
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
# ------------------------------------------------------------------------------

import json
import urllib.request as urllib
from urllib.error import URLError, HTTPError

from sawtooth_cli.exceptions import CliException


class RestClient(object):
    def __init__(self, base_url=None):
        self._base_url = base_url or 'http://localhost:8080'

    def list_blocks(self):
        return self._get('/blocks')['data']

    def get_block(self, block_id):
        safe_id = urllib.quote(block_id, safe='')
        return self._get('/blocks/' + safe_id)['data']

    def _get(self, path):
        try:
            response = urllib.urlopen(self._base_url + path)
        except HTTPError as e:
            raise CliException('({}) {}'.format(e.code, e.msg))
        except URLError as e:
            raise CliException(
                ('Unable to connect to "{}" '
                 'make sure URL is correct').format(self._base_url))
        result = response.read().decode('utf-8')
        return json.loads(result)
