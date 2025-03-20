from tkinter import ttk, Misc
import tkinter as tk
from typing import Iterable
from comps.component import Component
from lib import event_bus as eb
from lib.image_manager import ImageManager
from lib.logger import log
from comps import email_preview_toolbar
from database import Database
from models import EmailModel, EmailStatus


class AttachmentSidebarPopupMenu(tk.Menu):
    def __init__(self, parent: Misc):
        super().__init__(parent)

        self.add_command(label="Open", command=lambda: eb.bus.publish("attachment_sidebar.popup_menu.open_option#click"))
        self.add_command(label="Remove", command=lambda: eb.bus.publish("attachment_sidebar.popup_menu.remove_option#click"))

class AttachmentSidebar(Component):

    popup_menu: AttachmentSidebarPopupMenu

    def __init__(self, parent: Misc):
        Component.__init__(self, parent, label=__name__)

        self.popup_menu = AttachmentSidebarPopupMenu(self)

        self.drop_in = Component(self, label="drop_in")
        self.drop_in.pack(side="top", expand=False)

        ttk.Label(self.drop_in, text="Drop-In").pack(padx=20, pady=20, anchor="center")

        self.attach_list = Component(self, label="attachments")
        self.attach_list.pack(side="bottom", expand=True)
        
        self.tree = ttk.Treeview(self.attach_list, show="tree")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<Button-3>", self._on_right_click)

        eb.bus.subscribe("email_editor.attachments#selected", self._on_attach_button_click)
        eb.bus.subscribe("email_editor.send_button#no_attachments.click", self._on_send_button_click)
        eb.bus.subscribe("attachment_sidebar.popup_menu.open_option#click", self._on_popup_menu_open_click)
        eb.bus.subscribe("attachment_sidebar.popup_menu.remove_option#click", self._on_popup_menu_remove_click)
        eb.bus.subscribe(email_preview_toolbar.EventNames.EDIT, self._on_email_preview_edit_click)


    def _on_email_preview_edit_click(self, e: eb.Event):
        log.info("-------------------------------------------")

        # remove the items in the tree
        # show attachs of the current draft email in the tree
        
        email = e.data["email"]
        assert isinstance(email, EmailModel) and email.status == EmailStatus.DRAFT

        db = Database()
        attchs = db.fetch_attachments_by_email_id(email.email_id)

        log.info(f"Attachments of email {email}:")
        log.info(attchs)

        self.tree.delete(*self.tree.get_children())
        for a in attchs:
            self.tree.insert("", "end", text=a.filepath)
        
        log.info("-------------------------------------------")
        return False



    def _on_popup_menu_open_click(self, e: eb.Event):
        selected_ids = self.tree.selection()
        for id in selected_ids:
            filepath = self.tree.item(id, "text")
            log.info("Open attachment:", filepath)

        return True

    def _on_popup_menu_remove_click(self, e: eb.Event):
        selected_ids = self.tree.selection()
        self.tree.delete(*selected_ids)

        return True

    def _on_right_click(self, e: tk.Event):
        identifier = self.tree.identify_row(e.y)
        if identifier:
            self.tree.selection_add(identifier)
            self.popup_menu.tk_popup(e.x_root, e.y_root)


    def _on_attach_button_click(self, e: eb.Event):
        attachments = e.data["attachments"]

        img = ImageManager()

        for attachment in attachments: 
            self.tree.insert("", "end", text=attachment, image=img.get("icon_attachment"))

        return True

    def _on_send_button_click(self, e: eb.Event):
        editor_data = e.data

        editor_data["attachments"] = self.get_attachments()

        eb.bus.publish("attachment_sidebar.send_button#with_attachment.click", data=editor_data)
        return True

    def get_attachments(self):
        return [self.tree.item(item_id, "text") for item_id in self.tree.get_children()]

    def clear_attachment_list(self):
        attchs: list[str] = []
        for item_id in self.tree.get_children():
            attchs.append(self.tree.item(item_id, "text"))
            self.tree.delete(item_id)
        return attchs
    
    def add_attachment(self, attachment: str):
        self.tree.insert("", "end", text=attachment)

    def add_attachments(self, attachments: list[str]):
        for a in attachments:
            self.tree.insert("", "end", text=a)

        


