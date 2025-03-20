from dataclasses import dataclass
from enum import StrEnum
import re
from tkinter import END, Text, ttk, Misc, StringVar, filedialog
from typing import Callable, Dict, Iterable, List, Literal, LiteralString, Tuple, Union, override
from comps.component import Component
from lib.image_manager import ImageManager
from lib import event_bus as eb


class EventNames(StrEnum):
    SEND_BUTTON_CLICK = "email_editor.send_button#no_attachments.click"
    SAVE_BUTTON_CLICK = "email_editor.save_button#click"
    ATTACH_BUTTON_CLICK = "email_editor.attach_button#click"



class HeaderEntry(ttk.Entry):
    var: StringVar
    
    def __init__(self, parent: Misc, var: StringVar, *args, **kwargs):
        super().__init__(parent, textvariable=var, *args, **kwargs)
        self.var = var


class EmailEditor(Component):
    is_valid_recepient_email: bool
    toolbar_frame: Component
    header_frame: Component
    body_frame: Component

    def __init__(self, parent: Misc):
        Component.__init__(self, parent, label=__name__)

        self.is_valid_recepient_email = False

        img = ImageManager()

        self.editor_comps: Dict[str, Component] = {}

        self.toolbar_frame = Component(self, "toolbar_frame")
        self.header_frame = Component(self, "header_frame")
        self.body_frame = Component(self, "body_frame")

        # toolbar_frame
        ttk.Button(
            self.toolbar_frame, 
            text="Send", 
            image=img.get("icon_send"), 
            compound="left", 
            style="LeftAlign.TButton", 
            command=self.on_send_button_click).pack(side="left", padx=10, pady=10)

        ttk.Button(
            self.toolbar_frame, 
            text="Save", 
            image=img.get("icon_save"), 
            compound="left", 
            style="LeftAlign.TButton", 
            command=self.on_save_button_click).pack(side="left", padx=10, pady=10)

        ttk.Button(
            self.toolbar_frame, 
            text="Attach", 
            image=img.get("icon_attach_file"), 
            compound="left", style="LeftAlign.TButton",
            command=lambda: eb.bus.publish(EventNames.ATTACH_BUTTON_CLICK)).pack(side="right", padx=10, pady=10)

        
        # header_frame
        self.entries: Dict[str, HeaderEntry] = {
            "sender": HeaderEntry(self.header_frame, var=StringVar(value="tra0163@vsb.cz"), state="readonly"),
            "recipients": HeaderEntry(self.header_frame, var=StringVar(value=""), state="enabled"),
            "subject": HeaderEntry(self.header_frame, var=StringVar(value=""), state="enabled"),
        }
        
        # bind the email validation
        self.entries["recipients"].bind("<KeyRelease>", lambda _: self.check_email(self.entries["recipients"].get()))

        self.header_frame.grid_columnconfigure(1, weight=1)

        for index, (label, entry) in enumerate(self.entries.items()):
            ttk.Label(self.header_frame, text=label.capitalize(), anchor="e").grid(row=index+1, column=0, padx=10, pady=(0, 5), sticky="ew")
            entry.grid(row=index+1, column=1, padx=10, pady=(0, 5), sticky="ew")
            # entry.var.trace_add("write", lambda name, index, mode, var=entry.var: print(name, mode, var.get()))


        # body_frame 
        self.textarea = Text(self.body_frame, width=48, height=12, highlightthickness=0, borderwidth=1, border=1)

        textarea_scrollbar = ttk.Scrollbar(self.body_frame, orient="vertical", command=self.textarea.yview)
        self.textarea.configure(yscrollcommand=textarea_scrollbar.set)

        self.textarea.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        textarea_scrollbar.pack(side="right", fill="y", padx=(0, 5), pady=10)


        # parent: email_editor
        self.toolbar_frame.pack(expand=False)
        self.header_frame.pack(pady=0, expand=False)
        self.body_frame.pack()

        # events
        eb.bus.subscribe(EventNames.ATTACH_BUTTON_CLICK, self.on_attach_button_click)


    def on_attach_button_click(self, _: eb.Event):
        attachments = filedialog.askopenfilenames()

        eb.bus.publish("email_editor.attachments#selected", data={
            "attachments": attachments
        })

        return True

    
    def get_content(self):
        data: Dict[str, bool | str | Iterable[str]] = {}
        
        data["sender_email"] = self.entries["sender"].get()
        data["subject"] = self.entries["subject"].get()
        data["body"] = self.textarea.get(1.0, "end")
        data["recipients"] = { self.entries["recipients"].get() }
        
        return data


    def on_send_button_click(self):
        error_messages: List[str] = []

        data = self.get_content()
        
        if not self.is_valid_recepient_email:
            error_messages.append("recipient's email not valid")

        if not data["subject"]:
            error_messages.append("missing subject")

        if len([c for c in data["body"] if not c.isspace()]) == 0:
            error_messages.append("missing body")

        data["valid"] = len(error_messages) == 0
        data["errors"] = error_messages

        eb.bus.publish(EventNames.SEND_BUTTON_CLICK, data=data)
        return True

    def on_save_button_click(self):
        data = self.get_content()
        eb.bus.publish(EventNames.SAVE_BUTTON_CLICK, data=data)
        return True


    def check_email(self, new_emails_value: str):
        emails = new_emails_value.split(",")
        regex = r"^([a-zA-Z0-9][a-zA-Z0-9._%+-]{0,63}[a-zA-Z0-9]@(?:[a-zA-Z0-9-]{1,63}\.){1,125}[a-zA-Z]{2,63}$)"

        self.is_valid_recepient_email = True

        for email in emails:
            self.is_valid_recepient_email = re.match(regex, email.strip(" ")) is not None

        foreground = "red" if not self.is_valid_recepient_email else ""
        self.entries["recipients"].configure(foreground=foreground)

        return self.is_valid_recepient_email


    def clear_entries(self):
        entries: dict[str, str] = {}
        for k, e in self.entries.items():
            entries[k] = e.var.get()
            e.var.set("")

        return entries


    def clear_body(self):
        current_state = self.textarea.cget("state")
        self.textarea.configure(state="normal")
        body = self.textarea.get(1.0, "end")
        self.textarea.delete(1.0, "end")
        self.textarea.configure(state=current_state)
        return body

    
    def insert_body(self, body: str):
        current_state = self.textarea.cget("state")
        self.textarea.configure(state="normal")
        self.textarea.delete(1.0, "end")
        self.textarea.insert(1.0, body)
        self.textarea.configure(state=current_state)
        

    def insert_entries(self, entries: dict[str, Union[str, list[str]]]):
        for k,v in entries.items():
            self.entries[k].var.set(", ".join(v) if isinstance(v, list) else v)


    @override
    def enable(self):
        super().enable()
        self.entries["sender"].configure(state="readonly")

