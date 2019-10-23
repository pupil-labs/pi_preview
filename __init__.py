import logging
from collections import namedtuple

logger = logging.getLogger(__name__)

try:
    from ndsi import __version__

    assert __version__ >= "1.0"
    from ndsi import __protocol_version__
except (ImportError, AssertionError):
    raise Exception("pyndsi version is to old. Please upgrade") from None

GAZE_SENSOR_TYPE = "gaze"
Linked_Device = namedtuple("Linked_Device", ["uuid", "name"])

from pi_preview._plugin import PI_Preview
