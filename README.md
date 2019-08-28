# hstspreload

Chromium HSTS Preload list as a Python package and updated daily.

Install via `python -m pip install hstspreload`

See https://hstspreload.org for more information regarding the list itself.

## API

The package provides a single function: `in_hsts_preload()` which takes an
IDNA-encoded host and returns either `True` or `False` regarding whether
that host should be only accessed via HTTPS.

## Changelog

This script gathers the HSTS Preload list by monitoring
[this file in the Chromium repository](https://github.com/chromium/chromium/blob/master/net/http/transport_security_state_static.json).
Changes to the HSTS Preload list can be seen in the
[history of that file](https://github.com/chromium/chromium/commits/master/net/http/transport_security_state_static.json).

## License

BSD-3
