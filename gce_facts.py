#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

DOCUMENTATION = '''
---
module: gce_facts
short_description: Gathers facts about instances within Google Cloud infrastructure
version_added: "1.0"
options:
description:
     - This module fetches data from the metadata servers in Google Cloud as per
       https://cloud.google.com/compute/docs/metadata.
       The module must be called from within the GCE instance itself.
       Module based on the code written by Silviu Dicu <silviudicu@gmail.com>.
notes:
    - Module is in alpha stage, facts format *will* be changed without prior notification.
author: "Vasiliy Kaygorodov <vkaygorodov@gmail.com>"
'''

EXAMPLES = '''
# Conditional example
- name: Gather instance GCE facts
  action: gce_facts

- name: Conditional
  action: debug msg="This instance is scheduled to restart automatically"
  when: ansible_gce_scheduling_automatic_restart == "TRUE"
'''

import socket
import re

socket.setdefaulttimeout(5)

class GceMetadata(object):

    gce_metadata_uri = 'http://metadata.google.internal/computeMetadata/v1/instance/'

    def __init__(self, module, gce_metadata_uri=None):
        self.module   = module
        self.uri_meta = gce_metadata_uri or self.gce_metadata_uri
        self._data     = {}
        self._prefix   = 'ansible_gce_%s'

    def _fetch(self, url):
        (response, info) = fetch_url(self.module, url, headers={ "Metadata-Flavor": "Google" }, force=True)
        if response:
            data = response.read()
        else:
            data = None
        return data

    def _mangle_fields(self, fields, uri):
        new_fields = {}
        for key, value in fields.iteritems():
            split_fields = key[len(uri):].split('/')
            if len(split_fields) > 1 and split_fields[1]:
                new_key = "-".join(split_fields)
                new_fields[self._prefix % new_key] = value
            else:
                new_key = "".join(split_fields)
                new_fields[self._prefix % new_key] = value
        return new_fields

    def fetch(self, uri, recurse=True):
        raw_subfields = self._fetch(uri)
        if not raw_subfields:
            return
        subfields = raw_subfields.split('\n')
        for field in subfields:
            if field.endswith('/') and recurse:
                self.fetch(uri + field)
            if uri.endswith('/'):
                new_uri = uri + field
            else:
                new_uri = uri + '/' + field
            if new_uri not in self._data and not new_uri.endswith('/'):
                content = self._fetch(new_uri)
                self._data['%s' % (new_uri)] = content

    def fix_invalid_varnames(self, data):
        """Change ':'' and '-' to '_' to ensure valid template variable names"""
        for (key, value) in data.items():
            if ':' in key or '-' in key:
                newkey = key.replace(':','_').replace('-','_')
                del data[key]
                data[newkey] = value

    def run(self):
        self.fetch(self.uri_meta) # populate _data
        data = self._mangle_fields(self._data, self.uri_meta)
        self.fix_invalid_varnames(data)
        return data

def main():
    argument_spec = url_argument_spec()

    module = AnsibleModule(
        argument_spec = argument_spec,
        supports_check_mode = True,
    )

    gce_facts = GceMetadata(module).run()
    gce_facts_result = dict(changed=False, ansible_facts=gce_facts)

    module.exit_json(**gce_facts_result)

# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

main()
