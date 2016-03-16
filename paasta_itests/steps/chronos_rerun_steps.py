# Copyright 2015 Yelp Inc.
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
from behave import when

from paasta_tools.utils import _run


@when('we run chronos_rerun for service_instance {service_instance}')
def run_chronos_rerun(context, service_instance):
    print 'hello, world'
    cmd = (
        "python ../paasta_tools/chronos_rerun.py -d %s '%s' "
        "2016-03-13T04:50:31"
    ) % (context.soa_dir, service_instance)
    exit_code, output = _run(cmd)
    context.exit_code, context.output = exit_code, output
