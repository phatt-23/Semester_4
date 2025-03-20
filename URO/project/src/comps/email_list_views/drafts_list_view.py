from tkinter import Misc
from comps.email_list_views.email_list_view import EmailListView
import database as db
from lib import event_bus as eb
from comps import email_editor
from models import EmailModel, EmailStatus
from debug import DEFAULT_LOGGED_IN_EMAIL

class DraftsListView(EmailListView):
    def __init__(self, parent: Misc):
        super().__init__(parent, label=__name__)

        eb.bus.subscribe(db.EventNames.EMAIL_WITH_RECIPIENTS_AND_ATTACHMENTS_INSERT, self._on_email_recipient_and_attachments)
        eb.bus.subscribe(email_editor.EventNames.SAVE_BUTTON_CLICK, self._on_save_draft)

        self.populate_list()
   
    def _on_save_draft(self, e: eb.Event):
        # db.db.insert_email_with_recipients_and_attachments(
        #     e.data["sender_email"],
        #     e.data["subject"],
        #     e.data["body"],
        #     e.data["recipients"],
        #     attachments=[],
        #     status=EmailStatus.DRAFT
        # )
        return False

    def _on_email_recipient_and_attachments(self, e: eb.Event):
        email = e.data["email"]
        assert isinstance(email, EmailModel)

        sender = db.db.fetch_user_by_id(email.sender_id)
        assert sender

        self.add_email(sender, email, index=0)

        return False

    def populate_list(self):
        user = db.db.fetch_user_by_email(DEFAULT_LOGGED_IN_EMAIL)
        assert user
        emails = db.db.fetch_emails_from_user(user.user_id)
        for e in emails:
            if e.status == EmailStatus.DRAFT:
                self.add_email(user, e, index=0)
            

