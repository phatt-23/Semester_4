import tkinter as tk
from tkinter import ttk

class MyApp:
    def __init__(self, root):
        self.root = root

        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="Back", command=root.quit)
        self.menu.add_command(label="Quit", command=root.quit)
        # root.config(menu=self.menu)

        self.frame = tk.Frame(self.root, width=300, height=200)
        self.frame.pack()
        self.frame.bind("<Button-3>", self.popup)


    def popup(self, event):
        print(event)
        self.menu.post(event.x_root, event.y_root)


root = tk.Tk()
app = MyApp(root)
root.mainloop()
