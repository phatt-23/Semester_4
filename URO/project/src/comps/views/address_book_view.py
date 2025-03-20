from tkinter import ttk, Misc
from comps.component import Component
from database import Database

class AddressBookView(Component):
    def __init__(self, parent: Misc):
        Component.__init__(self, parent, label=__name__)

        columns = ("email", "first_name", "last_name")
        treeview = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse")
        for column in columns:
            text = " ".join([c.capitalize() for c in column.replace("_", " ").split(" ")])
            treeview.heading(column=column, text=text)

        db = Database()
        for user in db.fetch_all_users():
            treeview.insert("", "end", values=(user.email, user.first_name, user.last_name))

        treeview.pack()
