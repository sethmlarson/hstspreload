"""Builds the hstspreload.bin file"""

import base64
import datetime
import hashlib
import json
import re
import struct
import sys

import urllib3

from hstspreload import _INCLUDE_SUBDOMAINS, _IS_LEAF, _crc8

HSTS_PRELOAD_URL = (
    "https://chromium.googlesource.com/chromium/src/+/master/"
    "net/http/transport_security_state_static.json?format=TEXT"
)
VERSION_RE = re.compile(r"^__version__\s+=\s+\"[\d.]+\"", re.MULTILINE)
CHECKSUM_RE = re.compile(r"^__checksum__\s+=\s+\"([a-f0-9]*)\"", re.MULTILINE)
JUMPTABLE_RE = re.compile(r"^_JUMPTABLE\s+=\s+[^\n]+$", re.MULTILINE)


def main():
    print("Downloading latest HSTS preload list...")
    http = urllib3.PoolManager()
    r = http.request(
        "GET",
        HSTS_PRELOAD_URL,
        headers={"Accept": "application/json"},
        preload_content=True,
    )
    content = base64.b64decode(r.data)
    content_checksum = hashlib.sha256(content).hexdigest()
    content = content.decode("ascii")
    print("Checksum of downloaded list is: %s" % content_checksum)

    with open("hstspreload/__init__.py", "r") as f:
        data = f.read()
    current_checksum = CHECKSUM_RE.search(data).group(1)
    print("Checksum of current list is: %s" % current_checksum)
    if current_checksum == content_checksum:
        print("Detected no changes to HSTS preload list, cancelling build...")
        return 1

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
                checksum = _crc8(label)
                labs = layers.setdefault((i, checksum), set())
                labs.add(
                    (
                        is_leaf,
                        include_subdomains if is_leaf else False,
                        name if is_leaf else label,
                    )
                )

    print("Encoding labels into binary...")
    bin_layers = {}
    for layer in range(4):
        for checksum in range(256):
            chunks = []
            for is_leaf, include_subdomains, label in sorted(
                layers.get((layer, checksum), []),
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

            bin_layers[(layer, checksum)] = b"".join(chunks)

    print("Encoding layer offsets into jump table...")
    jump_table = []
    current_offset = 0
    for layer in range(4):
        jump_table_for_layer = []
        for checksum in range(256):
            bin_layer = bin_layers[(layer, checksum)]
            if not bin_layer:
                jump_table_for_layer.append((None, 0))
            else:
                layer_len = len(bin_layer)
                jump_table_for_layer.append((current_offset, layer_len))
                current_offset += layer_len
        jump_table.append(jump_table_for_layer)

    print("Writing data into hstspreload.bin...")
    with open("hstspreload/hstspreload.bin", "wb") as f:
        f.truncate()
        for layer in range(4):
            for checksum in range(256):
                f.write(bin_layers[(layer, checksum)])

    print("Updating __version__, __checksum__ and _JUMPTABLE...")
    with open("hstspreload/__init__.py", "r") as f:
        data = f.read()
    today = datetime.date.today()
    data = VERSION_RE.sub(
        '__version__ = "%d.%d.%d"' % (today.year, today.month, today.day), data, re.M
    )
    data = CHECKSUM_RE.sub('__checksum__ = "%s"' % content_checksum, data)
    data = JUMPTABLE_RE.sub("_JUMPTABLE = %s  # noqa: E501" % str(jump_table), data)
    with open("hstspreload/__init__.py", "w") as f:
        f.truncate()
        f.write(data)

    return 0


if __name__ == "__main__":
    sys.exit(main())
