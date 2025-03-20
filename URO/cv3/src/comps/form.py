from typing import Callable, Optional
from observer import Observer, Observable
import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
from data import ContactInfo, PostalInfo
from comps.contact_tree import ContactTreeComp 

class ContactInfoFormComp(Observer, Observable):

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

        self.mainFrame = tk.Frame(self.parent)

        # creating entries
        self.basicContactInfoFrame = tk.Frame(self.mainFrame)

        self.birthCertificateEntry = tk.Entry(self.basicContactInfoFrame)
        self.firstNameEntry = tk.Entry(self.basicContactInfoFrame)
        self.lastNameEntry = tk.Entry(self.basicContactInfoFrame)
        self.phoneNumberEntry = tk.Entry(self.basicContactInfoFrame)

        # creating notebooks for adding postal info and notes
        self.notebook = ttk.Notebook(self.mainFrame)

        # postal info tab
        # self.postalInfoTabFrame = tk.LabelFrame(self.notebook, labelwidget=tk.Label(text="Postal Info Tab"))
        self.postalInfoTabFrame = tk.Frame(self.notebook)
        # self.postalInfoFormFrame = tk.LabelFrame(self.postalInfoTabFrame, labelwidget=tk.Label(text="Postal Info Frame"))
        self.postalInfoFormFrame = tk.Frame(self.postalInfoTabFrame)

        self.streetEntry = tk.Entry(self.postalInfoFormFrame, width=24)
        self.cityEntry = tk.Entry(self.postalInfoFormFrame, width=24)
        self.streetNumberEntry = tk.Entry(self.postalInfoFormFrame, width=8)
        self.postalCodeEntry = tk.Entry(self.postalInfoFormFrame, width=8)

        self.includePostalInfoButton = tk.Checkbutton(self.postalInfoFormFrame, text="Don't want to provide postal info", variable=self.includePostalInfo)

        # notes tab
        # self.notesTabFrame = tk.LabelFrame(self.notebook, labelwidget=tk.Label(text="Notes Tab"))
        self.notesTabFrame = tk.Frame(self.notebook)
        self.notesTabText = tk.Text(self.notesTabFrame, height=8, width=48)

        self.notebook.add(child=self.postalInfoTabFrame, text="Postal Info")
        self.notebook.add(child=self.notesTabFrame, text="Notes")

        # binding actions to events
        # parent.bind("<Key-Return>", lambda _: self.onAddButtonClick())
        self.buttonFrame = tk.Frame(self.mainFrame)

        self.cancelButton = tk.Button(self.buttonFrame, text="Cancel", command=self.clearContactEntries)
        self.editButton = tk.Button(self.buttonFrame, text="Edit", command=self.onEditContactEntry)
        self.addButton = tk.Button(self.buttonFrame, text="Add", command=self.onAddContactEntry)

        def insertDummyInitialContactInfo():
            self.firstNameEntry.insert(0, "Jan")
            self.lastNameEntry.insert(0, "Novak")
            self.phoneNumberEntry.insert(0, "720 183 294")
            self.birthCertificateEntry.insert(0, "192168100")

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
            contact = ContactInfo(self.firstNameEntry.get(), self.lastNameEntry.get(), self.phoneNumberEntry.get(), self.birthCertificateEntry.get(), postalInfo)
            self.onEditCallback(contact)
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
            contact = ContactInfo(self.firstNameEntry.get(), self.lastNameEntry.get(), self.phoneNumberEntry.get(), self.birthCertificateEntry.get(), postalInfo)
            self.onAddCallback(contact)
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
        self.birthCertificateEntry.delete(0, tk.END)

        if not self.includePostalInfo.get():
            self.streetEntry.delete(0, tk.END)
            self.streetNumberEntry.delete(0, tk.END)
            self.cityEntry.delete(0, tk.END)
            self.postalCodeEntry.delete(0, tk.END)


    def pack(self):
        # postal info form tab
        self.postalInfoFormFrame.columnconfigure(1, weight=1)
        self.postalInfoFormFrame.columnconfigure(3, weight=0)  # set 0 to prevent from growing

        tk.Label(self.postalInfoFormFrame, text="Street:")          .grid(row=0, column=0, sticky=tk.E)
        self.streetEntry                                            .grid(row=0, column=1, sticky=tk.EW)
        tk.Label(self.postalInfoFormFrame, text="Street Number:")   .grid(row=0, column=2, sticky=tk.E)
        self.streetNumberEntry                                      .grid(row=0, column=3, sticky=tk.W)

        tk.Label(self.postalInfoFormFrame, text="City:")            .grid(row=1, column=0, sticky=tk.E)
        self.cityEntry                                              .grid(row=1, column=1, sticky=tk.EW)
        tk.Label(self.postalInfoFormFrame, text="Postal Code:")     .grid(row=1, column=2, sticky=tk.E)
        self.postalCodeEntry                                        .grid(row=1, column=3, sticky=tk.W)

        self.includePostalInfoButton.grid(row=2, column=0, columnspan=4, sticky='w')

        self.postalInfoFormFrame.pack(padx=10, pady=10, anchor="center")


        # notebook with postal info tab and notes tab
        self.notesTabText.pack()


        # main contact info form
        tk.Label(self.basicContactInfoFrame, text="First Name:")        .grid(row=0, column=0, sticky=tk.E)
        self.firstNameEntry                                             .grid(row=0, column=1)
        tk.Label(self.basicContactInfoFrame, text="Last Name:")         .grid(row=1, column=0, sticky=tk.E)
        self.lastNameEntry                                              .grid(row=1, column=1)
        tk.Label(self.basicContactInfoFrame, text='Birth Certificate:') .grid(row=2, column=0, sticky=tk.E)
        self.birthCertificateEntry                                      .grid(row=2, column=1)
        tk.Label(self.basicContactInfoFrame, text="Phone:")             .grid(row=3, column=0, sticky=tk.E)
        self.phoneNumberEntry                                           .grid(row=3, column=1)


        # confirmation and cancelation buttons 
        self.cancelButton.pack(side='left')
        self.editButton.pack(side='left')
        self.addButton.pack(side='left')


        # parents
        self.basicContactInfoFrame  .grid(row=0,column=0,padx=10)
        self.buttonFrame            .grid(row=1,column=0,padx=10)
        self.notebook               .grid(row=0,column=1,rowspan=2,padx=10)
        
        self.mainFrame.pack(anchor='center', padx=10, pady=10, expand=True)


    def update(self, observable, *args, **kwargs):
        print("ContactInfoFormComponent update")

        if isinstance(observable, ContactTreeComp):
            values = kwargs["selectedItemValues"]
            print(values)

            self.clearContactEntries()

            try:
                birthCert, firstName, lastName, phoneNumber, street, streetNumber, city, postalCode = values
                self.streetEntry.insert(0, street)
                self.streetNumberEntry.insert(0, streetNumber)
                self.cityEntry.insert(0, city)
                self.postalCodeEntry.insert(0, postalCode)
            except Exception as _:
                birthCert, firstName, lastName, phoneNumber = values
            
            self.firstNameEntry.insert(0, firstName)
            self.lastNameEntry.insert(0, lastName)
            self.phoneNumberEntry.insert(0, phoneNumber)
            self.birthCertificateEntry.insert(0, birthCert)

