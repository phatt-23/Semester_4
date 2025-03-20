#!/usr/bin/env python3

from typing import Callable, Optional
from observer import Observer, Observable
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font
import json

from utils import print_hierarchy
from data import ContactInfo, PostalInfo
from comps.contact_tree import ContactTreeComp
from comps.main_menu_bar import MainMenuBarComp
from comps.form import ContactInfoFormComp


class App:
    window: tk.Tk
    contacts: list[ContactInfo]

    def __init__(self, root: tk.Tk):
        # setting initial values
        self.window = root
        self.contacts = ContactInfo.sampleData()
        self.filepath = "contacts.json"

        self.window.title("Contact Info")

        mainFrame = tk.Frame(self.window)
        # mainFrame = tk.LabelFrame(self.window, labelwidget=tk.Label(text="Main"))

        self.contactsTreeViewFrame = tk.Frame(mainFrame)
        # self.contactsTreeViewFrame = tk.LabelFrame(mainFrame, labelwidget=tk.Label(text="Contact Tree"))
        self.contactTreeComp = ContactTreeComp(self.contactsTreeViewFrame)

        # contactEntryFrame = tk.LabelFrame(mainFrame, labelwidget=tk.Label(text="Contact Entry"))
        contactEntryFrame = tk.Frame(mainFrame)
        contactFormComp = ContactInfoFormComp(
            contactEntryFrame,
            onAdd=lambda contact: self.onAddContactToContactTree(
                self.contactTreeComp, contact
            ),
            onEdit=lambda contact: self.onEditContactInContactTree(
                self.contactTreeComp, contact
            ),
        )

        mainMenuBar = MainMenuBarComp(
            self.window,
            onQuit=lambda: self.window.destroy(),
            onSave=self.onMenuSave,
            onOpen=self.onMenuOpen,
            onClearAll=self.onMenuClearAll,
            onViewNames=lambda: self.contactTreeComp.viewColumns(
                ["birthCertificate", "firstName", "lastName", "phone"]
            ),
            onViewAddresses=lambda: self.contactTreeComp.viewColumns(
                ["birthCertificate", "street", "streetNumber", "city", "postalCode"]
            ),
            onViewNamesAndAddresses=lambda: self.contactTreeComp.viewColumns(
                self.contactTreeComp.getColumns()
            ),
        )
        login = tk.Label(mainFrame, text="tra0163", font=font.BOLD)

        self.contactTreeComp.addObserver(contactFormComp)

        for c in self.contacts:
            self.contactTreeComp.insertContact(c)

        # render
        self.contactTreeComp.pack()
        self.contactsTreeViewFrame.pack(expand=True, fill="both")

        contactFormComp.pack()
        contactEntryFrame.pack(fill="x", expand=True)
        login.pack(anchor=tk.SE)

        mainMenuBar.pack()
        mainFrame.pack(padx=20, pady=20, fill="both", expand=True)

    def onEditContactInContactTree(
        self, contactTreeComp: ContactTreeComp, contact: ContactInfo
    ):
        contactTree = contactTreeComp.getTreeview()

        focusedItem = contactTree.focus()
        index = contactTree.index(item=focusedItem)

        if focusedItem:
            contactTree.delete(focusedItem)
            contactTreeComp.insertContact(contact, index)

    def onAddContactToContactTree(
        self, contactTreeComp: ContactTreeComp, contact: ContactInfo
    ):
        print("on insert contact to contact tree:", *contact)
        self.contacts.append(contact)
        contactTreeComp.getTreeview().insert("", tk.END, values=(*contact,))

    def onMenuClearAll(self):
        # delete everything from the tree view
        for c in self.contactTreeComp.getTreeview().get_children():
            self.contactTreeComp.getTreeview().delete(c)

    def onMenuSave(self):
        jsonString = json.dumps(
            [json.loads(c.toJson()) for c in self.contacts], indent=4
        )
        with open(self.filepath, "w") as f:
            print(f"saved into file: {self.filepath}")
            f.write(jsonString)

    def onMenuOpen(self):
        parsedContacts = []

        with open(self.filepath, "r") as f:
            print(f"reading from file: {self.filepath}")
            parsedContacts = [ContactInfo.fromJson(c) for c in json.loads(f.read())]

        self.contacts = parsedContacts

        # delete everything from the tree view
        for c in self.contactTreeComp.getTreeview().get_children():
            self.contactTreeComp.getTreeview().delete(c)

        # and insert the parsed contacts
        for c in self.contacts:
            self.contactTreeComp.insertContact(c)


if __name__ == "__main__":
    root = tk.Tk()

    s = ttk.Style(root)
    print(s.theme_names())
    print(s.theme_use())
    s.theme_use("clam")
    s.configure("clam", font='helvetica 24', foreground='red', padding=10)

    app = App(root)
    print_hierarchy(root)
    root.mainloop()
