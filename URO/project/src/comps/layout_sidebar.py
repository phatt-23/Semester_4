from dataclasses import dataclass
from tkinter import Misc, ttk
from typing import Dict
from comps.component import Component

from lib import event_bus as eb
from lib.image_manager import ImageManager


class EventNames:
    MAIL = "layout_sidebar.mail_view_button#click"
    COMPOSE = "layout_sidebar.compose_view_button#click"
    ADDRESS_BOOK = "layout_sidebar.address_book_view_button#click"
    CALENDAR = "layout_sidebar.calendar_view_button#click"

@dataclass
class ButtonConfig:
    parent: Misc
    event_name: str 
    icon_image_key: str


def publishing_button(text: str, config: ButtonConfig) -> ttk.Button:
    custom_style = "LeftAlign.TButton"
    style = ttk.Style()
    style.configure(custom_style, anchor="w")

    return ttk.Button(
        config.parent, 
        text=" ".join([word.capitalize() for word in text.split("_")]),
        command=lambda: eb.bus.publish(config.event_name), 
        image=ImageManager().get(config.icon_image_key),
        compound="left",
        style=custom_style
    )


class LayoutSidebar(Component):
    def __init__(self, parent: Misc):
        Component.__init__(self, parent, label=__name__)

        self.top_frame = ttk.Frame(self)

        buttons_configs = {
            "mail"         : ButtonConfig(self.top_frame, EventNames.MAIL, "icon_email"),
            "compose"      : ButtonConfig(self.top_frame, EventNames.COMPOSE, "icon_create"),
            "address_book" : ButtonConfig(self.top_frame, EventNames.ADDRESS_BOOK, "icon_contacts"),
            "calendar"     : ButtonConfig(self.top_frame, EventNames.CALENDAR, "icon_calendar_month"),
        }

        self.top_buttons: Dict[str, ttk.Button] = {}

        for name, config in buttons_configs.items():
            self.top_buttons[name] = publishing_button(name, config)

        self.logout_btn = publishing_button("Log-Out", ButtonConfig(self, "layout_sidebar.logout_button#click", "icon_logout"))

        eb.bus.subscribe("email_preview_toolbar.edit_button#click", self._on_email_preview_toolbar_edit_click)

    def _on_email_preview_toolbar_edit_click(self, e: eb.Event):
        self.top_buttons["compose"].invoke()
        return False


    def render(self):
        for _, button in self.top_buttons.items():
            button.pack(anchor="n", pady=2, fill="x", expand=True)

        self.top_frame.pack(anchor="n", fill="x", padx=10, pady=10, expand=True)
        self.logout_btn.pack(anchor="s", padx=10, pady=10, fill="x", expand=True)
