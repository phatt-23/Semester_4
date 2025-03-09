#!/usr/bin/env python

from typing import Callable, Optional

import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
from tkinter import font
import json


class Observer:

    def update(self, obervable, *args, **kwargs):
        pass


class Observable:

    callbacks: list[Callable[[], None]]
    observers: list[Observer]

    def __init__(self):
        self.observers = []
        self.callbacks = []

    def addObserver(self, observer: Observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def removeObserver(self, observer: Observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def addCallback(self, callback: Callable[[], None]):
        if callback not in self.callbacks:
            self.callbacks.append(callback)

    def removeCallback(self, callback: Callable[[], None]):
        if callback in self.callbacks:
            self.callbacks.remove(callback)

    def notifyObservers(self, *args, **kwargs):
        for observer in self.observers:
            observer.update(self, *args, **kwargs)

        for callback in self.callbacks:
            callback()


class PostalInfo():
    street: str
    streetNumber: str
    city: str
    postalCode: str

    def __init__(self, street: str = '', streetNumber: str = '', city: str = '', postalCode: str = ''):
        self.street = street
        self.streetNumber = streetNumber
        self.city = city
        self.postalCode = postalCode

    def __str__(self):
        return f"street: {self.street}, streetNumber: {self.streetNumber}, city: {self.city}, postalCode: {self.postalCode}"

    def __iter__(self):
        return iter((self.street, self.streetNumber, self.city, self.postalCode))

    def toJson(self):
        json.dumps(self, default=lambda o: o.__dict__)

    @staticmethod
    def fromJson(data):
        if not data:
            return None

        return PostalInfo(
            data.get("street", ""),
            data.get("streetNumber", ""),
            data.get("city", ""),
            data.get("postalCode", "")
        )


class ContactInfo():
    firstName: str
    lastName: str
    phoneNumber: str
    postalInfo: Optional[PostalInfo]

    def __init__(self, firstName='', lastName='', phoneNumber='', postalInfo: Optional[PostalInfo] = None):
        self.firstName = firstName
        self.lastName = lastName
        self.phoneNumber = phoneNumber
        self.postalInfo = postalInfo 

    def __str__(self):
        return f"firstName: {self.firstName}, lastName: {self.lastName}, phoneNumber: {self.phoneNumber}, postalInfo: {self.postalInfo}"

    def __iter__(self):
        return iter((self.firstName, self.lastName, self.phoneNumber, *self.postalInfo)) if self.postalInfo \
                else iter((self.firstName, self.lastName, self.phoneNumber))

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    @staticmethod
    def fromJson(data: dict):
        return ContactInfo(
            data.get("firstName", ""),
            data.get("lastName", ""),
            data.get("phoneNumber", ""),
            PostalInfo.fromJson(data.get("postalInfo"))
        )

    @staticmethod
    def sampleData():
        return [
            ContactInfo("John", "Doe", "+1-555-1234", PostalInfo("Main Street", "42", "New York", "10001")),
            ContactInfo("Alice", "Smith", "+44-20-7946-0958", PostalInfo("Baker Street", "221B", "London", "NW1 6XE")),
            ContactInfo("Tom", "Brown", "+49-30-1234567"),  # No postal info
            ContactInfo("Marie", "Curie", "+33-1-2345-6789", PostalInfo("Rue de la Science", "7", "Paris", "75005")),
            ContactInfo("Liam", "Johnson", "+1-617-555-7890", PostalInfo("Boylston St", "500", "Boston", "02116")),
            ContactInfo("Emma", "Williams", "+61-2-5551-4321", PostalInfo("George St", "80", "Sydney", "2000")),
            ContactInfo("Noah", "Davis", "+81-3-5555-6789", PostalInfo("Shibuya", "15-7", "Tokyo", "150-0002")),
            ContactInfo("Olivia", "Martinez", "+34-91-555-9876", PostalInfo("Gran Via", "23", "Madrid", "28013")),
            ContactInfo("James", "Taylor", "+1-415-555-2468", PostalInfo("Market St", "870", "San Francisco", "94103")),
            ContactInfo("Sophia", "Anderson", "+49-89-555-1357", PostalInfo("Marienplatz", "1", "Munich", "80331")),
            ContactInfo("Mason", "Hernandez", "+55-11-5555-2468"),  # No postal info
            ContactInfo("Isabella", "Lopez", "+39-06-5555-8642", PostalInfo("Via del Corso", "18", "Rome", "00186")),
        ]


class MainMenuBarComponent():

    onSaveCallback: Optional[Callable[[], None]]
    onOpenCallback: Optional[Callable[[], None]]
    onQuitCallback: Optional[Callable[[], None]]
    onClearAllCallback: Optional[Callable[[], None]]

    def __init__(self, window: tk.Tk, 
                 onSave: Optional[Callable[[], None]]=None,
                 onOpen: Optional[Callable[[], None]]=None,
                 onQuit: Optional[Callable[[], None]]=None,
                 onClearAll: Optional[Callable[[], None]]=None):

        self.window = window
        self.mainMenuBar = tk.Menu(window)

        self.onSaveCallback = onSave
        self.onOpenCallback = onOpen
        self.onQuitCallback = onQuit
        self.onClearAllCallback = onClearAll

        fileMenu = tk.Menu(self.mainMenuBar, tearoff=tk.FALSE)
        fileMenu.add_command(label="Save", command=self._onSave)
        fileMenu.add_command(label="Open", command=self._onOpen)
        fileMenu.add_command(label="Quit", command=self._onQuit)
        self.mainMenuBar.add_cascade(label="File", menu=fileMenu)

        editMenu = tk.Menu(self.mainMenuBar, tearoff=tk.FALSE)
        editMenu.add_command(label="Clear All", command=self._onClearAll)
        self.mainMenuBar.add_cascade(label="Edit", menu=editMenu)

        helpMenu = tk.Menu(self.mainMenuBar, tearoff=tk.FALSE)
        helpMenu.add_command(label="Insertion", command=lambda: print("help - insertion"))
        helpMenu.add_command(label="Deletion", command=lambda: print("help - deletion"))
        self.mainMenuBar.add_cascade(label="Help", menu=helpMenu)


    def _onSave(self):
        if self.onSaveCallback:
            self.onSaveCallback()


    def _onOpen(self):
        if self.onOpenCallback:
            self.onOpenCallback()


    def _onQuit(self):
        if self.onQuitCallback:
            self.onQuitCallback()

    def _onClearAll(self):
        if self.onClearAllCallback:
            self.onClearAllCallback()

    def pack(self):
        self.window.configure(menu=self.mainMenuBar)


    def get(self):
        return self.mainMenuBar


class ContactInfoFormComponent(Observer, Observable):

    onAddCallback: Optional[Callable[[ContactInfo], None]]
    onEditCallback: Optional[Callable[[ContactInfo], None]]

    includePostalInfo: tk.BooleanVar

    def __init__(self, parent: tk.Widget, 
                 onAdd: Optional[Callable[[ContactInfo], None]]=None, 
                 onEdit: Optional[Callable[[ContactInfo], None]]=None):
        Observer.__init__(self)
        Observable.__init__(self)

        self.includePostalInfo = tk.BooleanVar()

        self.parent = parent
        self.onAddCallback = onAdd
        self.onEditCallback = onEdit

        # creating entries
        self.basicContactInfoFrame = tk.Frame(parent)

        self.firstNameEntry = tk.Entry(self.basicContactInfoFrame)
        self.lastNameEntry = tk.Entry(self.basicContactInfoFrame)
        self.phoneNumberEntry = tk.Entry(self.basicContactInfoFrame)

        # creating notebooks for adding postal info and notes
        self.notebook = ttk.Notebook(parent)

        # postal info tab
        self.postalInfoTabFrame = tk.LabelFrame(self.notebook, labelwidget=tk.Label(text="Postal Info Tab"))
        self.postalInfoFormFrame = tk.LabelFrame(self.postalInfoTabFrame, labelwidget=tk.Label(text="Postal Info Frame"))

        self.streetEntry = tk.Entry(self.postalInfoFormFrame, width=40)
        self.streetNumberEntry = tk.Entry(self.postalInfoFormFrame)
        self.cityEntry = tk.Entry(self.postalInfoFormFrame)
        self.postalCodeEntry = tk.Entry(self.postalInfoFormFrame)

        self.includePostalInfoButton = tk.Checkbutton(self.postalInfoFormFrame, text="Don't want to provide postal info", variable=self.includePostalInfo)

        # notes tab
        self.notesTabFrame = tk.LabelFrame(self.notebook, labelwidget=tk.Label(text="Notes Tab"))
        self.notesTabText = tk.Text(self.notesTabFrame, height=10)

        self.notebook.add(child=self.postalInfoTabFrame, text="Postal Info")
        self.notebook.add(child=self.notesTabFrame, text="Notes")


        # binding actions to events
        # parent.bind("<Key-Return>", lambda _: self.onAddButtonClick())
        self.buttonFrame = tk.Frame(parent)

        self.cancelButton = tk.Button(self.buttonFrame, text="Cancel", command=self.clearContactEntries)
        self.editButton = tk.Button(self.buttonFrame, text="Edit", command=self.onEditContactEntry)
        self.addButton = tk.Button(self.buttonFrame, text="Add", command=self.onAddContactEntry)


        def insertDummyInitialContactInfo():
            self.firstNameEntry.insert(0, "Jan")
            self.lastNameEntry.insert(0, "Novak")
            self.phoneNumberEntry.insert(0, "720 183 294")

            self.streetEntry.insert(0, "Ulicka ulice")
            self.streetNumberEntry.insert(0, "12/34")
            self.cityEntry.insert(0, "Ostrava")
            self.postalCodeEntry.insert(0, "300 20")
        insertDummyInitialContactInfo()
    

    def onEditContactEntry(self):
        hadError, title, message = self.checkMissingFields()
        if hadError:
            messagebox.showerror(title="[EDIT]" + title, message=message)
            return

        if self.onEditCallback:
            postalInfo = None
            if not self.includePostalInfo.get():
                postalInfo = PostalInfo(self.streetEntry.get(), self.streetNumberEntry.get(), self.cityEntry.get(), self.postalCodeEntry.get())

            self.onEditCallback(ContactInfo(self.firstNameEntry.get(), self.lastNameEntry.get(), self.phoneNumberEntry.get(), postalInfo))
            self.clearContactEntries()


    def onAddContactEntry(self):
        hadError, title, message = self.checkMissingFields()
        if hadError:
            messagebox.showerror(title="[ADD]" + title, message=message)
            return
        
        if self.onAddCallback:
            postalInfo = None
            if not self.includePostalInfo.get():
                postalInfo = PostalInfo(self.streetEntry.get(), self.streetNumberEntry.get(), self.cityEntry.get(), self.postalCodeEntry.get())

            self.onAddCallback(ContactInfo(self.firstNameEntry.get(), self.lastNameEntry.get(), self.phoneNumberEntry.get(), postalInfo))
            self.clearContactEntries()


    def checkMissingFields(self):
        # confirm button 
        missingFields = []

        def addIfMissing(entry: tk.Entry, name): 
            if not entry.get():
                missingFields.append(name)

        addIfMissing(self.firstNameEntry, "First Name")
        addIfMissing(self.lastNameEntry, "Last Name")
        addIfMissing(self.phoneNumberEntry, "Phone Number")

        if not self.includePostalInfo.get():
            addIfMissing(self.streetEntry, "Street")
            addIfMissing(self.streetNumberEntry, "Street Number")
            addIfMissing(self.cityEntry, "City")
            addIfMissing(self.postalCodeEntry, "Postal Code")

        return len(missingFields) > 0, "Contact Info form isn't complete", "Please fill out these fields: " + ",".join(missingFields)


    def clearContactEntries(self):
        self.firstNameEntry.delete(0, tk.END)
        self.lastNameEntry.delete(0, tk.END)
        self.phoneNumberEntry.delete(0, tk.END)

        if not self.includePostalInfo.get():
            self.streetEntry.delete(0, tk.END)
            self.streetNumberEntry.delete(0, tk.END)
            self.cityEntry.delete(0, tk.END)
            self.postalCodeEntry.delete(0, tk.END)


    def pack(self):
        # postal info form tab

        # Configure grid column weights for resizing behavior
        tk.Label(self.postalInfoFormFrame, text="Street:")          .grid(row=0, column=0, sticky=tk.E)
        tk.Label(self.postalInfoFormFrame, text="Street Number:")   .grid(row=0, column=2, sticky=tk.E)
        tk.Label(self.postalInfoFormFrame, text="City:")            .grid(row=1, column=0, sticky=tk.E)
        tk.Label(self.postalInfoFormFrame, text="Postal Code:")     .grid(row=1, column=2, sticky=tk.E)

        self.streetEntry                                            .grid(row=0, column=1, sticky=tk.EW)
        self.streetNumberEntry                                      .grid(row=0, column=3, sticky=tk.EW)
        self.cityEntry                                              .grid(row=1, column=1, sticky=tk.EW)
        self.postalCodeEntry                                        .grid(row=1, column=3, sticky=tk.EW)

        self.includePostalInfoButton.grid(row=3, column=3)

        self.postalInfoFormFrame.pack(padx=40, pady=40, side=tk.TOP)


        # notebook with postal info tab and notes tab
        self.notesTabText.pack()
        self.notebook.grid(row=4, columnspan=2)


        # main contact info form
        tk.Label(self.basicContactInfoFrame, text="First Name:").grid(row=0, column=0, sticky=tk.E)
        self.firstNameEntry.grid(row=0, column=1)

        tk.Label(self.basicContactInfoFrame, text="Last Name:").grid(row=1, column=0, sticky=tk.E)
        self.lastNameEntry.grid(row=1, column=1)

        tk.Label(self.basicContactInfoFrame, text="Phone:").grid(row=3, column=0, sticky=tk.E) 
        self.phoneNumberEntry.grid(row=3, column=1) 

        self.basicContactInfoFrame.grid(row=2,columnspan=2)


        # confirmation and cancelation buttons 
        self.cancelButton.grid(row=0,column=0)
        self.editButton.grid(row=0,column=1)
        self.addButton.grid(row=0,column=2)

        self.buttonFrame.grid(row=6,columnspan=3)


    def update(self, observable, *args, **kwargs):
        print("ContactInfoFormComponent update")

        if isinstance(observable, ContactTreeComponent):
            values = kwargs["selectedItemValues"]
            print(values)

            self.clearContactEntries()

            try:
                firstName, lastName, phoneNumber, street, streetNumber, city, postalCode = values
                self.streetEntry.insert(0, street)
                self.streetNumberEntry.insert(0, streetNumber)
                self.cityEntry.insert(0, city)
                self.postalCodeEntry.insert(0, postalCode)
            except Exception as _:
                firstName, lastName, phoneNumber = values
            
            self.firstNameEntry.insert(0, firstName)
            self.lastNameEntry.insert(0, lastName)
            self.phoneNumberEntry.insert(0, phoneNumber)


class ContactTreeComponent(Observable):

    def __init__(self, parent: tk.Widget):
        Observable.__init__(self)
        self.contactTree = ttk.Treeview(parent, show="tree headings", columns=("firstName", 
                                                                               "lastName", 
                                                                               "phone", 
                                                                               "street", 
                                                                               "streetNumber", 
                                                                               "city", 
                                                                               "postalCode"))

        # hide the first column which is now used for tree folding
        self.contactTree.column("#0", width=0, stretch=tk.FALSE)

        # couple the treeView and the scrollbar
        self.contactTreeScrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.contactTree.yview)
        self.contactTree.configure(yscrollcommand=self.contactTreeScrollbar.set)

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
        self.contactTree.grid(row=0, column=0, sticky=tk.NSEW)
        self.contactTreeScrollbar.grid(row=0, column=1, sticky=tk.NS)


    def getTreeview(self):
        return self.contactTree


    def insertContact(self, contact: ContactInfo, index=-1):
        self.contactTree.insert('', index if index >= 0 else tk.END, values=(*contact, ))


class Application():
    window: tk.Tk  
    contacts: list[ContactInfo]

    def __init__(self, root: tk.Tk):
        # setting initial values
        self.window = root
        self.contacts = ContactInfo.sampleData()
        self.filepath = "contacts.json"

        self.window.title("Contact Info")

        mainMenuBar = MainMenuBarComponent(self.window, 
                                           onQuit=lambda: self.window.destroy(),
                                           onSave=self.onMenuSave,
                                           onOpen=self.onMenuOpen,
                                           onClearAll=self.onMenuClearAll)

        mainFrame = tk.LabelFrame(self.window, labelwidget=tk.Label(text="Main"))

        contactsTreeViewFrame = tk.LabelFrame(mainFrame, labelwidget=tk.Label(text="Contact Tree"))
        self.contactTreeComp = ContactTreeComponent(contactsTreeViewFrame)

        contactEntryFrame = tk.LabelFrame(mainFrame, labelwidget=tk.Label(text="Contact Entry"))
        contactFormComp = ContactInfoFormComponent(contactEntryFrame, 
                                                   onAdd=lambda contact: self.onAddContactToContactTree(self.contactTreeComp, contact),
                                                   onEdit=lambda contact: self.onEditContactInContactTree(self.contactTreeComp, contact))

        login = tk.Label(mainFrame, text="TRA0163", font=font.BOLD)

        self.contactTreeComp.addObserver(contactFormComp)


        for c in self.contacts:
            self.contactTreeComp.insertContact(c)

        # render
        self.contactTreeComp.pack()
        contactsTreeViewFrame.pack()

        contactFormComp.pack()
        contactEntryFrame.pack()
        login.pack(anchor=tk.SE)

        mainMenuBar.pack()
        mainFrame.pack()


    def onEditContactInContactTree(self, contactTreeComp: ContactTreeComponent, contact: ContactInfo):
        contactTree = contactTreeComp.getTreeview()

        focusedItem = contactTree.focus()
        index = contactTree.index(item=focusedItem)

        if focusedItem: 
            contactTree.delete(focusedItem)
            contactTreeComp.insertContact(contact, index)


    def onAddContactToContactTree(self, contactTreeComp: ContactTreeComponent, contact: ContactInfo):
        self.contacts.append(contact)
        print('on insert contact to contact tree:', *contact)
        contactTreeComp.getTreeview().insert('', tk.END, values=(*contact, ))


    def onMenuClearAll(self):
        # delete everything from the tree view
        for c in self.contactTreeComp.getTreeview().get_children():
            self.contactTreeComp.getTreeview().delete(c)


    def onMenuSave(self):
        jsonString = json.dumps([json.loads(c.toJson()) for c in self.contacts], indent=4)

        with open(self.filepath, "w") as f:
            f.write(jsonString)
            print(f"saved into file: {self.filepath}")


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
    app = Application(root)
    root.mainloop()


