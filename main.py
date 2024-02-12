import base64
import zlib
import json

def decode_vpn_config(encoded_config):
    # Remove the 'vpn://' prefix
    encoded_config = encoded_config.replace("vpn://", "")

    # Base64 decode
    ba = base64.urlsafe_b64decode(encoded_config + "==")

    # Check for the Qt 4-byte header and remove it before decompressing
    if len(ba) >= 4:
        # Extract the size of the uncompressed data
        qt_header = ba[:4]
        uncompressed_size = int.from_bytes(qt_header, 'big')
        # Only proceed if the size is reasonable to prevent memory issues
        if uncompressed_size > 0 and uncompressed_size < 100 * 1024 * 1024:  # Arbitrary 100MB limit for safety
            try:
                # Remove the first 4 bytes before decompression
                ba_uncompressed = zlib.decompress(ba[4:])
            except zlib.error as e:
                raise ValueError(f"Error decompressing data: {e}")
        else:
            raise ValueError("Uncompressed size is unreasonable: {}".format(uncompressed_size))
    else:
        raise ValueError("Data is too short to contain Qt header.")

    try:
        decoded_json = json.loads(ba_uncompressed.decode('utf-8'))
        return decoded_json
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        raise ValueError(f"Error parsing JSON: {e}")


def encode_vpn_config(decoded_json):
    """
    Encodes a Python dictionary to a VPN configuration string using Base64 and compression,
    replicating the behavior of Qt's qCompress and Base64UrlEncoding with OmitTrailingEquals,
    and prefixing with 'vpn://'.

    Args:
        decoded_json (dict): The Python dictionary to encode.

    Returns:
        str: The encoded VPN configuration string, prefixed with 'vpn://'.
    """
    # Convert the JSON object to a string
    json_str = json.dumps(decoded_json)

    # Encode the string to bytes
    json_bytes = json_str.encode('utf-8')

    # Compress the bytes
    compressed_data = zlib.compress(json_bytes)

    # Qt's qCompress adds a 4-byte header indicating the uncompressed data size,
    # which we need to add manually. Since zlib's compress does not include this,
    # we prepend it ourselves. Note: The size is in Big-Endian format.
    uncompressed_size = len(json_bytes)
    qt_header = uncompressed_size.to_bytes(4, 'big')
    qt_compressed_data = qt_header + compressed_data

    # Base64 encode, omitting the padding
    base64_encoded_data = base64.urlsafe_b64encode(qt_compressed_data).decode('utf-8').rstrip('=')

    # Prefix with 'vpn://'
    encoded_config = f"vpn://{base64_encoded_data}"

    return encoded_config


encoded_config = "vpn://"
decoded_config = decode_vpn_config(encoded_config)

decoded_json = {
    "containers": [
        {
            "awg": {
                "H1": "222057347",
                "H2": "1694671954",
                "H3": "1385416949",
                "H4": "842854865",
                "Jc": "7",
                "Jmax": "1000",
                "Jmin": "50",
                "S1": "33",
                "S2": "65",
                "last_config": "{...your JSON data...}",
                "port": "37573",
                "transport_proto": "udp"
            },
            "container": "amnezia-awg"
        }
    ],
    "defaultContainer": "amnezia-awg",
    "description": "VPN Server",
    "dns1": "1.1.1.1",
    "dns2": "1.0.0.1",
    "hostName": "45.60.13.37"
}
encoded_config = encode_vpn_config(decoded_json)



