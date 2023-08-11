#!/usr/bin/env python

# Copyright 2023 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Live Stream sample for getting an asset.
Example usage:
    python get_asset.py --project_id <project-id> --location <location> --asset_id <asset-id>
"""

# [START livestream_get_asset]

import argparse

from google.cloud.video import live_stream_v1
from google.cloud.video.live_stream_v1.services.livestream_service import (
    LivestreamServiceClient,
)


def get_asset(
    project_id: str, location: str, asset_id: str
) -> live_stream_v1.types.Asset:
    """Gets an asset.
    Args:
        project_id: The GCP project ID.
        location: The location of the asset.
        asset_id: The user-defined asset ID."""

    client = LivestreamServiceClient()

    name = f"projects/{project_id}/locations/{location}/assets/{asset_id}"
    response = client.get_asset(name=name)
    print(f"Asset: {response.name}")

    return response


# [END livestream_get_asset]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", help="Your Cloud project ID.", required=True)
    parser.add_argument(
        "--location",
        help="The location of the asset.",
        required=True,
    )
    parser.add_argument(
        "--asset_id",
        help="The user-defined asset ID.",
        required=True,
    )
    args = parser.parse_args()
    get_asset(
        args.project_id,
        args.location,
        args.asset_id,
    )
