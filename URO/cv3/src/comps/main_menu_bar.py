from os import wait
import tkinter as tk
from typing import Optional, Callable


class MainMenuBarComp:
    onSaveCallback: Optional[Callable[[], None]]
    onOpenCallback: Optional[Callable[[], None]]
    onQuitCallback: Optional[Callable[[], None]]
    onClearAllCallback: Optional[Callable[[], None]]
    onViewNames: Optional[Callable[[], None]]
    onViewAddresses: Optional[Callable[[], None]]
    onViewNamesAndAddresses: Optional[Callable[[], None]]

    def __init__(
        self,
        window: tk.Tk,
        onSave: Optional[Callable[[], None]] = None,
        onOpen: Optional[Callable[[], None]] = None,
        onQuit: Optional[Callable[[], None]] = None,
        onClearAll: Optional[Callable[[], None]] = None,
        onViewNames: Optional[Callable[[], None]] = None,
        onViewAddresses: Optional[Callable[[], None]] = None,
        onViewNamesAndAddresses: Optional[Callable[[], None]] = None,
    ):
        self.window = window
        self.mainMenuBar = tk.Menu(window)
        self.onSaveCallback = onSave
        self.onOpenCallback = onOpen
        self.onQuitCallback = onQuit
        self.onClearAllCallback = onClearAll
        self.onViewNames = onViewNames
        self.onViewAddresses = onViewAddresses
        self.onViewNamesAndAddresses = onViewNamesAndAddresses

        fileMenu = tk.Menu(self.mainMenuBar, tearoff=tk.FALSE)
        viewMenu = tk.Menu(self.mainMenuBar, tearoff=tk.FALSE)
        editMenu = tk.Menu(self.mainMenuBar, tearoff=tk.FALSE)

        fileMenu.add_command(
            label="Save",
            command=lambda: self.onSaveCallback() if self.onSaveCallback else None,
        )
        fileMenu.add_command(
            label="Open",
            command=lambda: self.onOpenCallback() if self.onOpenCallback else None,
        )
        fileMenu.add_command(
            label="Quit",
            command=lambda: self.onQuitCallback() if self.onQuitCallback else None,
        )
        self.mainMenuBar.add_cascade(label="File", menu=fileMenu)

        viewMenu.add_command(
            label="Names",
            command=lambda: self.onViewNames() if self.onViewNames else None,
        )
        viewMenu.add_command(
            label="Addresses",
            command=lambda: self.onViewAddresses() if self.onViewAddresses else None,
        )
        viewMenu.add_command(
            label="Names and Addresses",
            command=lambda: self.onViewNamesAndAddresses()
            if self.onViewNamesAndAddresses
            else None,
        )
        self.mainMenuBar.add_cascade(label="View", menu=viewMenu)

        editMenu.add_command(
            label="Clear All",
            command=lambda: self.onClearAllCallback()
            if self.onClearAllCallback
            else None,
        )
        self.mainMenuBar.add_cascade(label="Edit", menu=editMenu)

        helpMenu = tk.Menu(self.mainMenuBar, tearoff=tk.FALSE)
        helpMenu.add_command(
            label="Insertion", command=lambda: print("help - insertion")
        )
        helpMenu.add_command(label="Deletion", command=lambda: print("help - deletion"))
        self.mainMenuBar.add_cascade(label="Help", menu=helpMenu)

    def pack(self):
        self.window.configure(menu=self.mainMenuBar)

    def get(self):
        return self.mainMenuBar
