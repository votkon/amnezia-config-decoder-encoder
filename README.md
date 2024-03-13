# VPN Config Codec

Welcome to the VPN Config Codec repository! This toolkit is designed to encode and decode VPN configurations using a combination of compression, base64 encoding, and JSON serialization techniques. It's ideal for developers and system administrators who need a reliable method to share and manage VPN settings in a compact, URL-friendly string format.

## Getting Started

To use this toolkit, you will need Python installed on your machine. The script is compatible with Python 3.x versions.

## Features

- **Encoding VPN Configurations**: Convert detailed VPN configurations stored in Python dictionaries into compressed, base64-encoded strings, prefixed with `vpn://`. This method facilitates easy sharing and distribution of VPN settings.
- **Decoding VPN Configurations**: Decode the previously encoded VPN configuration strings back into Python dictionaries, allowing for easy interpretation and modification of VPN settings.

## How to Use

### Encode a VPN Configuration

1. Prepare your VPN configuration as a Python dictionary.
2. Call `encode_vpn_config(decoded_json)` with your dictionary.
3. The function returns a `vpn://` prefixed, base64-encoded string representing your VPN configuration.

### Decode a VPN Configuration

1. Obtain an encoded VPN configuration string (ensure it starts with `vpn://`).
2. Call `decode_vpn_config(encoded_config)` with this string.
3. The function returns the original Python dictionary containing the VPN configuration.

## Example

Here's a quick example to demonstrate the encoding and decoding process:

```python
from vpn_config_codec import encode_vpn_config, decode_vpn_config

# Example VPN configuration dictionary
decoded_json = {
    "hostName": "example.com",
    "port": 1194,
    "protocol": "udp",
    "encryption": "AES-256-CBC",
    "auth": "SHA256"
}

# Encode the configuration
encoded_config = encode_vpn_config(decoded_json)
print("Encoded:", encoded_config)

# Decode the configuration
decoded_config = decode_vpn_config(encoded_config)
print("Decoded:", decoded_config)
