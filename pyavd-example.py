#!/usr/bin/env python3
from pathlib import Path

from pyavd import (
    get_device_config,
    validate_structured_config,
)


def write_device_config(hostname: str, avd_structured_config: dict, output_path: Path, strict: bool = False):

    validation_result = validate_structured_config(avd_structured_config)
    if validation_result.failed and strict:
        raise RuntimeError(f"{hostname} validate_structured_config failed")

    # Write device configs
    with open(f"{output_path}/{hostname}.cfg", mode="w", encoding="utf8") as fd:
        fd.write(get_device_config(avd_structured_config))


if __name__ == "__main__":
    hostname = "my_device"
    my_device_structured_config = {
        "hostname": "my_device",
        "is_deployed": True,
        "ip_routing": True,
        "management_interfaces": [
            {
                "name": "Management1",
                "description":"OOB Management Interface",
                "shutdown": False,
                "vrf": "MGMT",
                "ip_address": "10.10.10.20/24",
                "gateway": "10.10.10.1",
                "type": "oob"
            }
        ],
        "static_routes": [
            {
                "vrf": "MGMT",
                "destination_address_prefix": "0.0.0.0/0",
                "gateway": "10.10.10.1"
            }
        ],
        "vrfs": [
            {
                "name": "MGMT",
                "ip_routing": False
            }
        ],
        "ip_name_servers": [
            {
                "ip_address": "10.100.163.10",
                "vrf": "MGMT"
            }
        ],
        "ntp": {
            "local_interface": {
                "name": "Management1",
                "vrf": "MGMT"
            },
            "servers": [
                {
                    "name": "0.pool.ntp.org",
                    "vrf": "MGMT"
                }
            ]
        },
        "loopback_interfaces": [
            {
                "name": "Loopback0",
                "description": "EVPN_Overlay_Peering",
                "shutdown": False,
                "ip_address": "10.255.0.3/32"
            }
        ]
    }

    write_device_config(hostname, my_device_structured_config, "output", True)
