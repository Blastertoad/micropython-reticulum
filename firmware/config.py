"""
µReticulum — Node Configuration
================================
Edit this file to configure your node. Uncomment the interface(s) you need.
"""

from lora_boards import LORA_BOARDS

# ---- Node settings ----
WIFI_SSID = "AP"
WIFI_PASS = "pass"
NODE_NAME = "ESP32s3"

# DEBUG levels: 0 = silent, 1 = messages & announces only, 2 = full debug
DEBUG = 2


# ---- Reticulum config ----
# All interfaces are listed below. Uncomment the ones you want to use.
# Multiple interfaces can be active at the same time (e.g. WiFi + LoRa).
CONFIG = {
    "loglevel": 3,
    "enable_transport": False,

    # LoRa board pinout presets (see firmware/lora_boards.py). An interface
    # below references one with "board": "<name>"; the preset's pins are merged
    # in at startup. Edit lora_boards.py to add a board — no other changes.
    "lora_boards": LORA_BOARDS,

    # Dedicated destination that replies to `rnprobe` (reference RNS tool).
    # Set "enabled": True to expose the probe destination. See README.
    "probe": {
        "enabled": False,
        "app_name": "urns",            # full_name = "urns.probe"
        "aspect": "probe",
        "announce_interval": 60 * 60,  # 1 hour; 0 = announce once at boot only
    },

    # ---- Time sync ----
    # Pure-LoRa nodes have no RTC or NTP, so their clock sits at 2000-01-01 and
    # every outgoing message/announce is stamped "Jan 2000". With time sync
    # enabled, the node learns the real time ONCE per boot from a trusted
    # peer it overhears — either an announce timestamp or a signature-validated
    # LXMF message timestamp. After that the ESP32's internal RTC keeps time
    # for the rest of the power-on session (a reboot resets it, then it
    # re-syncs from the next trusted packet).
    #
    # Two modes:
    #   - Authority: list LXMF delivery destination hashes (hex, exactly as
    #     shown in MeshChat/Sideband) in trusted_nodes. One matching source
    #     sets the clock immediately.
    #   - Corroboration: leave trusted_nodes empty. The clock is set only once
    #     `min_sources` distinct peers agree on the time within `tolerance`
    #     seconds (the median is applied). No single node can set it alone.
    "time_sync": {
        "enabled": True,
        "trusted_nodes": [
            # "a1b2c3d4e5f60718293a4b5c6d7e8f90",   # e.g. your phone's MeshChat address
        ],
        "min_sources": 2,      # corroboration quorum when trusted_nodes is empty
        "tolerance": 120,      # seconds; max clock disagreement between peers
    },

    "interfaces": [

        # ---- WiFi UDP ----
        # Broadcasts on the local LAN. Works with MeshChat / Sideband.
        # Set forward_ip to None for auto-detected subnet broadcast.
          {
              "type": "UDPInterface",
              "name": "WiFi UDP",
              "enabled": True,
              "listen_ip": "0.0.0.0",
              "listen_port": 4242,
              "forward_ip": "255.255.255.255",
              "forward_port": 4242,
          },

        # ---- SX1262 SPI LoRa (micropython-lib lora-sx126x driver) ----
        # Install: mpremote mip install lora-sx126x
        #
        # The board's pins come from a preset in lora_boards.py — just set
        # "board" to its name. Only network/radio params live here, and they
        # must match on every node of the mesh:
        #   freq_khz: 868000 (EU), 915000 (US), 923000 (AS)
        #   sf: 7-12 (higher = longer range, slower)
        #   bw: "125"/"250"/"500" (lower = longer range, slower)
        #   tx_power: -9 to +22 dBm     syncword: 0x1424 (Reticulum/RNode)
        #
        # Available board presets (see lora_boards.py):
        #   "xiao_esp32s3_sx1262"          XIAO ESP32-S3 + Wio-SX1262 (kit)
        #   "xiao_esp32s3_sx1262_header"   XIAO ESP32-S3 + Wio-SX1262 (header)
        #   "esp32s3_cam_sx1262"           ESP32-S3 WROOM CAM + Wio-SX1262
        #   "HTIT-WB32LAF"                 Heltec V4 LoRa HTIT-WB32LAF + SX-1262 embedded
        #
        # Any pin can still be overridden inline (it wins over the preset).
        #
        {
            "type": "LoRaInterface",
            "board": "HTIT-WB32LAF",
            "name": "Heltec V4 LoRa",
            "enabled": True,
            "freq_khz": 915000,
            "sf": 8,
            "bw": "125",
            "coding_rate": 5,
            "tx_power": 28,
            "preamble_len": 8,
            "crc_en": True,
            "syncword": 0x1424,
        },

        # ---- TCP Client ----
        # Connects to a remote RNS TCP server (TCPServerInterface).
        # Uses HDLC framing, wire-compatible with reference Reticulum.
        {
           "type": "TCPClientInterface",
           "name": "TestComputer",
           "enabled": True,
           "target_host": "192.168.1.101",
           "target_port": 4243,
        },

        # ---- Serial (for RNode / wired link) ----
        # {
        #     "type": "SerialInterface",
        #     "name": "Serial Link",
        #     "enabled": True,
        #     "uart_id": 1,
        #     "tx_pin": 17,
        #     "rx_pin": 16,
        #     "speed": 115200,
        # },

    ],
}

# ---- Sensor Network config ----
# LXMF Destination address for data to be sent to
SENSOR_HUB = ""
