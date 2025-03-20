import tkinter as tk
from tkinter import ttk, Misc, Canvas
from comps.component import Component
from database import Database
from models import EmailModel, UserModel
from comps.email_card_list import EmailCardList
from lib import event_bus as eb
from comps.email_list_views.email_list_view import EmailListView
from comps.email_list_views.inbox_list_view import InboxListView
from comps.email_list_views.sent_mail_list_view import SentMailListView
from comps.email_list_views.drafts_list_view import DraftsListView
from comps.email_list_views.all_mail_list_view import AllMailListView 
from comps.email_list_views.spam_list_view import SpamListView 
from comps.email_list_views.bin_list_view import BinListView 
from comps.search_bar import SearchBar


class EmailList(Component):
    list_views: dict[str, EmailListView] 
    current_list_view: EmailListView 

    def __init__(self, parent: Misc):
        Component.__init__(self, parent, label=__name__)

        self.search_bar = SearchBar(self)

        self.list_views = {
            "inbox": InboxListView(self),
            "drafts": DraftsListView(self),
            "sent_mail": SentMailListView(self),
            "all_mail": AllMailListView(self),
            "spam": SpamListView(self),
            "bin": BinListView(self),
        }

        # default to inbox
        self.current_list_view = self.list_views["inbox"]
        
        # events
        eb.bus.subscribe("category_list.item#click", self._on_view_item_click)

    def _on_view_item_click(self, e: eb.Event):

        view_name = e.data["item_name"]
        self.current_list_view.pack_forget()
        self.current_list_view = self.list_views[view_name]
        self.current_list_view.pack()

        return True
        
    def render(self):
        self.search_bar.pack(expand=False)
        self.current_list_view.pack()


