from observer import Observable
import tkinter as tk
from tkinter import ttk
from data import ContactInfo


class ContactTreeComp(Observable):
    def __init__(self, parent: tk.Widget):
        Observable.__init__(self)

        self.parent = parent

        columns = (
            "birthCertificate",
            "firstName",
            "lastName",
            "phone",
            "street",
            "streetNumber",
            "city",
            "postalCode",
        )

        displayColumns = ("birthCertificate", "firstName", "lastName", "phone")

        self.mainFrame = tk.Frame(self.parent)
        # self.mainFrame = tk.LabelFrame(self.parent, labelwidget=tk.Label(text="Main Frame"))

        self.contactTree = ttk.Treeview(
            self.mainFrame, show="tree headings", columns=columns, displaycolumns=displayColumns
        )

        # hide the first column which is now used for tree folding
        self.contactTree.column("#0", width=0, stretch=tk.FALSE)

        # couple the treeView and the scrollbar
        self.contactTreeScrollbar = ttk.Scrollbar(
            self.mainFrame, orient=tk.VERTICAL, command=self.contactTree.yview
        )
        self.contactTree.configure(yscrollcommand=self.contactTreeScrollbar.set)

        self.contactTree.heading("birthCertificate", text="Birth Certificate")
        self.contactTree.heading("firstName", text="First Name")
        self.contactTree.heading("lastName", text="Last Name")
        self.contactTree.heading("phone", text="Phone Number")
        self.contactTree.heading("street", text="Street")
        self.contactTree.heading("streetNumber", text="Street Number")
        self.contactTree.heading("city", text="City")
        self.contactTree.heading("postalCode", text="Postal Code")

        self.contactTree.bind("<ButtonRelease-1>", self.onLeftButtonClick)

    def onLeftButtonClick(self, event: tk.Event):
        selectedItem = self.contactTree.focus()
        if not selectedItem:
            return
        selectedItemValues = self.contactTree.item(selectedItem, "values")
        self.notifyObservers(self, selectedItemValues=selectedItemValues)

    def pack(self):
        self.contactTree.pack(side='left', expand=True, fill='both')
        self.contactTreeScrollbar.pack(side='right', expand=True, fill='both')
        self.mainFrame.pack(fill='y', expand=True, pady=20)

    def getTreeview(self):
        return self.contactTree

    def insertContact(self, contact: ContactInfo, index=-1):
        self.contactTree.insert("", index if index >= 0 else tk.END, values=(*contact,))

    def get(self):
        return self.contactTree

    def getColumns(self):
        return self.contactTree["columns"]

    def viewColumns(self, columns: list[str]):
        self.contactTree.configure(displaycolumns=columns)

