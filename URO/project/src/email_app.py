#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Dict, Iterable, Tuple
from tkinter import messagebox, ttk
import lib.event_bus as eb
import tkinter as tk
from pathlib import Path
from preferences import FontBuilder
from vendor import sv_ttk

from modals import ModalSendNonValidEmail, ModalShowHierarchy, ModalShowWidgetInfo
from lib.utils import get_hierarchy_string
from lib.application import Application
from lib.image_manager import ImageManager
from lib.logger import log
from database import Database
from comps.layout_sidebar import LayoutSidebar
from comps.layout_view import LayoutView
from comps.menubar import MenuBar
from comps.statusbar import StatusBar


class EmailClientApp(Application):
    def __init__(self):
        super().__init__()

        sv_ttk.set_theme("dark")

        font_settings = FontBuilder().size("normal").weight("bold").build()

        self.tk_instance.option_add("*Font", font_settings)

        style = ttk.Style()
        style.configure(".", font=font_settings)
        widget_types = [
            "TLabel", "TButton", "TEntry", "TText", "TCombobox",
            "TCheckbutton", "TMenubutton", "TNotebook", "TFrame",
            "TListbox", "TSpinbox", "TScrollbar", "TProgressbar",
            "TRadiobutton", "Treeview", "Menu", "Entry"
        ]
        for widget in widget_types:
            style.configure(widget, font=font_settings)


        Database().__init__()
        self.load_assets()

        self.tk_instance.geometry("1400x800")

        self.menubar = MenuBar(self.tk_instance)
        self.layout_sidebar = LayoutSidebar(self.main_frame)
        self.layout_view = LayoutView(self.main_frame)
        self.statusbar = StatusBar(self.tk_instance)

        eb.bus.subscribe_pattern("[a-zA-Z0-9._#]*", self.on_event)

    def on_event(self, e: eb.Event) -> bool:
        log.info(f"Event: {e}")

        match e.name:
            case "menu_bar.file_menu.quit_button#click":
                if messagebox.askyesno(title="Quit program", message="Do you really want to quit?"):
                    self.tk_instance.destroy()

            case "menu_bar.debug_menu.show_hierarchy_button#click":
                ModalShowHierarchy(self.tk_instance)

            case "menu_bar.debug_menu.print_hierarchy_button#click":
                log.info("\n" + get_hierarchy_string(self.tk_instance))

            case "menu_bar.debug_menu.print_comp_detail_button#click":
                self.start_capture()

            case "app_widget_capture#caught":
                w = e.data.get("captured_widget")
                assert isinstance(w, tk.Widget), "Failed to captured a widget!"
                ModalShowWidgetInfo(self.tk_instance, w)

            case "attachment_sidebar.send_button#with_attachment.click":
                if not e.data["valid"]:
                    ModalSendNonValidEmail(self.tk_instance, e.data["errors"])
                    return True 
                
                sender_email = e.data["sender_email"]
                subject = e.data["subject"]
                body = e.data["body"]
                recipients = e.data["recipients"]
                attachments = e.data["attachments"]

                assert isinstance(sender_email, str)
                assert isinstance(subject, str)
                assert isinstance(body, str)
                assert isinstance(recipients, Iterable)
                assert isinstance(attachments, Iterable)

                Database().insert_email_with_recipients_and_attachments(sender_email, subject, body, recipients, attachments)
                return True

        return False

                
    def render(self):
        self.layout_sidebar.pack(side="left", expand=False)
        self.layout_view.pack(side="right")

    def load_assets(self):
        @dataclass
        class ImageWithSize:
            filepath: str
            size: Tuple[int, int]

        images: Dict[str, ImageWithSize] = {}
        
        # Icons
        image_icon_size = (16, 16)
        image_icons_directory = Path("assets/icons")
        for path in image_icons_directory.glob("[a-zA-Z0-9_]*.png"):
            if not path.is_file():
                continue

            filepath = str(path)
            extension = ".png"
            undesired = "_24dp_E3E3E3"
            undesired_sub_pos = filepath.find(undesired)
            extension_pos = filepath.find(extension)

            if undesired_sub_pos >= 0:
                key = filepath[:undesired_sub_pos]
            else:
                key = filepath[:extension_pos]

            key = "icon_" + key[key.rfind("/")+1:]

            images[key] = ImageWithSize(filepath, image_icon_size)
        
        # Load into the cetral manager
        for key, image in images.items():
            ImageManager().load(str(image.filepath), key, image.size)

