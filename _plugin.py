import logging

import glfw
from pyglui import ui

from plugin import Plugin

from pi_preview import Linked_Device
from pi_preview.connection import Connection

logger = logging.getLogger(__name__)

IMG_WIDTH = 1088
IMG_HEIGHT = 1080


class PI_Preview(Plugin):
    icon_chr = "PI"
    order = 0.02  # ensures init after all plugins

    def __init__(
        self, g_pool, linked_device=...,
    ):
        super().__init__(g_pool)

        if linked_device is ...:
            linked_device = Linked_Device(None, None)
        else:
            linked_device = Linked_Device(*linked_device)

        self.connection = Connection(linked_device, update_ui_cb=self.update_ndsi_menu,)
        self._num_prefix_elements = 0

    def recent_events(self, events):
        gaze = self.connection.fetch_data()

        if gaze:
            if "gaze" not in events:
                events["gaze"] = gaze
            else:
                events["gaze"].extend(gaze)

    def init_ui(self):
        self.add_menu()
        self.menu.label = "Pupil Invisible Preview"
        self.menu.append(ui.Info_Text("Connection settings"))
        self._num_prefix_elements = len(self.menu)
        self.update_ndsi_menu()

    def deinit_ui(self):
        self.remove_menu()

    def update_ndsi_menu(self):
        del self.menu[self._num_prefix_elements :]
        self.connection.add_ui_elements(self.menu)

    def cleanup(self):
        self.connection.close()
        self.connection = None

    def get_init_dict(self):
        return {
            "linked_device": self.connection.sensor.linked_device,
        }
