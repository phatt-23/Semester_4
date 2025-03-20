from tkinter import Misc

from lib import event_bus as eb
from comps.component import Component
from comps.email_card_list import EmailCardList
from database import Database
from debug import DEFAULT_LOGGED_IN_EMAIL
from models import EmailModel, EmailStatus
from comps.email_list_views.email_list_view import EmailListView


class SentMailListView(EmailListView):

    def __init__(self, parent: Misc):
        super().__init__(parent, label=__name__)

        identifier = "[a-zA-Z0-9_]+"
        eb.bus.subscribe_pattern(f"db.email#{identifier}", self._on_db_email_change)

        self._populate_list()

    def _on_db_email_change(self, e: eb.Event):
        email = e.data["email"]
        assert isinstance(email, EmailModel)

        sender = Database().fetch_user_by_id(email.sender_id)
        if not sender:
            return False

        self.add_email(sender, email, index=0)
        return False
        # self.clear_list()
        # self._populate_list()

    def _populate_list(self):
        db = Database()
        user = db.fetch_user_by_email(DEFAULT_LOGGED_IN_EMAIL)

        if not user:
            raise ValueError(f"ERROR: User with email '{DEFAULT_LOGGED_IN_EMAIL}' isnt in the database!")

        for email in db.fetch_emails_from_user(user.user_id):
            if email.status == EmailStatus.SENT:
                self.add_email(user, email)


