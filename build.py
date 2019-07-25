"""Builds the hstspreload.bin file"""

import base64
import datetime
import json
import struct
import re
import sys
import httpx
import hashlib
from hstspreload import _crc8, _IS_LEAF, _INCLUDE_SUBDOMAINS, _LAYER_HEADER_SIZE


HSTS_PRELOAD_URL = (
    "https://chromium.googlesource.com/chromium/src/+/master/"
    "net/http/transport_security_state_static.json?format=TEXT"
)
VERSION_RE = re.compile(r"^__version__\s+=\s+\"[\d.]+\"", re.MULTILINE)
CHECKSUM_RE = re.compile(r"^__checksum__\s+=\s+\"([a-f0-9]*)\"", re.MULTILINE)


def main():
    print("Downloading latest HSTS preload list...")
    r = httpx.request("GET", HSTS_PRELOAD_URL, verify=True)
    content = base64.b64decode(r.content)
    content_checksum = hashlib.sha256(content).hexdigest()
    content = content.decode("ascii")
    print("Checksum of downloaded list is: %s" % content_checksum)

    with open("hstspreload/__init__.py", "r") as f:
        data = f.read()
    current_checksum = CHECKSUM_RE.search(data).group(1)
    print("Checksum of current list is: %s" % current_checksum)
    if current_checksum == content_checksum:
        print("Detected no changes to HSTS preload list, cancelling build...")
        return 100

    print("Parsing HSTS preload entries...")
    entries = json.loads(
        "\n".join(
            [line for line in content.split("\n") if not line.strip().startswith("//")]
        )
    )["entries"]

    layers = {}

    for entry in entries:
        name = entry["name"].encode("ascii")
        labels = name.split(b".")[::-1]
        include_subdomains = entry.get("include_subdomains", False)
        force_https = entry.get("mode", "") == "force-https"

        if force_https:
            for i, label in enumerate(labels):
                is_leaf = i == (len(labels) - 1)
                offset = _crc8(label)
                labs = layers.setdefault((i, offset), set())
                labs.add(
                    (
                        is_leaf,
                        include_subdomains if is_leaf else False,
                        name if is_leaf else label,
                    )
                )

    print("Encoding labels into binary...")
    bin_layers = {}
    all_data = 0
    for offset in range(4):
        for checksum in range(256):
            chunks = []
            for is_leaf, include_subdomains, label in sorted(
                layers.get((offset, checksum), []),
                key=lambda x: (not x[0], x[1], 256 - len(x[2]), x[2]),
            ):
                flags = 0x00
                if is_leaf:
                    flags |= _IS_LEAF
                if include_subdomains:
                    flags |= _INCLUDE_SUBDOMAINS
                if len(label) > 0xFF:
                    raise ValueError("label too long for encoding scheme: %r" % label)
                chunks.append(struct.pack("<BB", flags, len(label)) + label)

            bin_layers[(offset, checksum)] = b"".join(chunks)
            all_data += len(b"".join(chunks))

    print("Encoding layer offsets into jump table...")
    bin_headers = {}
    per_layer = 0
    for offset in range(4):
        bin_headers[offset] = b""
        for checksum in range(256):
            layer = bin_layers[(offset, checksum)]
            if not layer:
                bin_headers[offset] += struct.pack("<IH", 0, 0)
            else:
                bin_headers[offset] += struct.pack(
                    "<IH",
                    ((3 - offset) * _LAYER_HEADER_SIZE)
                    + ((255 - checksum) * 6)
                    + per_layer,
                    len(layer),
                )
                per_layer += len(layer)

    print("Writing data into hstspreload.bin...")
    with open("hstspreload/hstspreload.bin", "wb") as f:
        f.truncate()
        for offset in range(4):
            f.write(bin_headers[offset])
        for offset in range(4):
            for checksum in range(256):
                f.write(bin_layers[(offset, checksum)])

    print("Updating __version__ and __checksum__...")
    with open("hstspreload/__init__.py", "r") as f:
        data = f.read()
    today = datetime.date.today()
    data = VERSION_RE.sub(
        '__version__ = "%d.%d.%d"' % (today.year, today.month, today.day), data, re.M
    )
    data = CHECKSUM_RE.sub('__checksum__ = "%s"' % content_checksum, data)
    with open("hstspreload/__init__.py", "w") as f:
        f.truncate()
        f.write(data)

    return 0


if __name__ == "__main__":
    sys.exit(main())
