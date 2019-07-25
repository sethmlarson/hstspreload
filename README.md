# hstspreload

Chromium HSTS Preload list as a Python package and updated daily.

Install via `python -m pip install hstspreload`

See https://hstspreload.org for more information regarding the list itself.

## API

The package provides a single function: `in_hsts_preload()` which takes an
IDNA-encoded host and returns either `True` or `False` regarding whether
that host should be only accessed via HTTPS.

## License

BSD-3
