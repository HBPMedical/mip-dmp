# Copyright 2023 The HIP team, University Hospital of Lausanne (CHUV), Switzerland & Contributors
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

"""Module that provides functions to support the modules of the `mip_dmp.process` sub-package."""

def is_number(s):
    """Check if a string is a number.

    Parameters
    ----------
    s : str
        String to check.

    Returns
    -------
    bool
        True if the string is a number, False otherwise.
    """
    try:
        float(s)
        return True
    except ValueError:
        return False