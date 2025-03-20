from tkinter import Misc, ttk
from comps.component import Component

from comps.category_list import CategoryList
from comps.email_list import EmailList 
from comps.email_preview import EmailPreview


class EmailView(Component):
    def __init__(self, parent: Misc):
        Component.__init__(self, parent, label=__name__)

        self.paned_window = ttk.PanedWindow(self, orient="horizontal")

        self.category_list = CategoryList(self)
        self.email_list = EmailList(self)
        self.email_preview = EmailPreview(self)

        for ch in (self.category_list, self.email_list, self.email_preview):
            self.paned_window.add(ch)

    def render(self):
        self.paned_window.pack(fill="both", expand=True, padx=10, pady=10)



