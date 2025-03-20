from tkinter import StringVar, ttk, Misc
from comps.component import Component
from lib.image_manager import ImageManager
from comps.utils.hover_popup import HoverPopupText


class SearchBar(Component):
    search_string: StringVar

    def __init__(self, parent: Misc):
        Component.__init__(self, parent, label=__name__)
        self.search_string = StringVar()

        img = ImageManager()

        self.search_icon = ttk.Label(self, image=img.get("icon_search"))
        self.search_entry = ttk.Entry(self, textvariable=self.search_string)

        self.filter_button = ttk.Button(self, text="Filter", image=img.get("icon_filter_alt"))

        HoverPopupText(self.search_icon, "Search Mail")
        HoverPopupText(self.search_entry, "Search Mail")
        HoverPopupText(self.filter_button, "Filter Mail")

    def render(self):
        self.search_icon.pack(side="left", padx=(10, 0), pady=4)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=10, pady=4)
        self.filter_button.pack(side="right", padx=(0, 10), pady=4)


