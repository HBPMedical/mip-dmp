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

"""`Setup.py` for mip_dmp."""

from os import path as op
from setuptools import setup
from mip_dmp import VERSION as __version__


def main():
    """Main function of the MIP Dataset Mapper ``setup.py``"""
    # Handle version
    root_dir = op.abspath(op.dirname(__file__))
    version = None
    cmdclass = {}
    if op.isfile(op.join(root_dir, "mip_dmp", "VERSION")):
        with open(op.join(root_dir, "mip_dmp", "VERSION")) as vfile:
            version = vfile.readline().strip()
    if version is None:
        version = __version__
    # Setup configuration
    setup(
        name="mip_dmp",
        version=version,
        cmdclass=cmdclass,
    )


if __name__ == "__main__":
    main()

