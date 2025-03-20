from abc import abstractmethod
from tkinter import Misc

from lib import event_bus as eb
from comps.component import Component
from comps.email_card_list import EmailCardList
from database import Database
from debug import DEFAULT_LOGGED_IN_EMAIL
from models import EmailModel, UserModel


class EmailListView(Component):
    email_card_list: EmailCardList

    def __init__(self, parent: Misc, label: str):
        super().__init__(parent, label=label)

        self.email_card_list = EmailCardList(self)

    def render(self):
        self.email_card_list.pack()

    def add_email(self, sender: UserModel, email: EmailModel, index=-1):
        self.email_card_list.add_card(sender, email, index)

    def clear_list(self):
        self.email_card_list.clear_all()

    @abstractmethod
    def populate_list(self):
        pass
