# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2024)
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

from __future__ import annotations

import streamlit as st
from streamlit.runtime.scriptrunner.script_requests import ScriptRequestType
from tests.delta_generator_test_case import DeltaGeneratorTestCase


class StopTest(DeltaGeneratorTestCase):
    def test_stop(self):
        st.stop()
        assert self.script_run_ctx.script_requests._state == ScriptRequestType.STOP