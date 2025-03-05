# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.font
from tkinter import messagebox


def clamp(x, low, high):
    if x > high:
        return high
    if x < low:
        return low
    return x


class MyApp:

    def convert(self, event=None):
        """
            Conversion Formula:
            °C = (°F - 32) ÷ (9/5)
        """
        
        value = 0

        try:
            value = float(self.entryInput.get())
        except ValueError as _:
            messagebox.showinfo("Invalid Input", "Please specify a NUMBER!")
            self.entryInput.delete(0, tk.END)
            return

        direction = self.direction.get()
        
        converted_value = value
        height = 0

        match direction:
            case 0:
                value = clamp(value, -20, 50)
                     
                celsius = value
                fahrenheit = celsius * 9/5 + 32
                converted_value = fahrenheit
                height = (celsius + 20)/(50 - (-20))
            case 1:
                value = clamp(value, 0, 120)

                fahrenheit = value
                celsius = (fahrenheit - 32) * 5/9
                converted_value = celsius
                height = fahrenheit/(120 - 0)

        self.entryOutput.delete(0, tk.END)
        self.entryOutput.insert(0, str(round(converted_value, 2)))
        self.entryInput.delete(0, tk.END)
        self.entryInput.insert(0, str(value))

        y_top, y_bottom, x_coord = 80, 292, 146
        self.canvas.coords(self.rect, x_coord, y_bottom, 152, y_bottom - (y_bottom - y_top) * height)


    def __init__(self, root):
        self.root = root
        self.root.title('Temperature Converter')
        self.root.resizable(False, False)
        self.root.bind("<Escape>", lambda event: self.root.destroy())

        font = tkinter.font.nametofont("TkDefaultFont")
        font.config(size=16)

        self.leftFrame = tk.Frame(root)
        self.rightFrame = tk.Frame(root)
        
        self.direction = tk.IntVar()
        self.direction.set(1) 

        self.directionFrame = tk.Frame(self.leftFrame, bd=4, relief=tk.RIDGE)
        self.radioButton1 = tk.Radiobutton(self.directionFrame, text="C -> F", variable=self.direction, value=0)
        self.radioButton2 = tk.Radiobutton(self.directionFrame, text="F -> C", variable=self.direction, value=1)

        self.entryFrame = tk.Frame(self.leftFrame, bd=4, relief=tk.RIDGE)
        self.inputLabel = tk.Label(self.entryFrame, text="Input")
        self.entryInput = tk.Entry(self.entryFrame, width=10, font=font)
        self.entryInput.bind("<Key-Return>", self.convert)
        self.convertButton = tk.Button(self.entryFrame, text="Convert", command=self.convert)

        self.outputLabel = tk.Label(self.entryFrame, text="Output")
        self.entryOutput = tk.Entry(self.entryFrame, width=10, font=font)
        self.entryOutput.insert(0, "No output")

        self.canvas = tk.Canvas(self.rightFrame, width=300, height=400)
        self.photo = tk.PhotoImage(file="th_empty.png")
        self.canvas.create_image(150, 200, image=self.photo)
        self.rect = self.canvas.create_rectangle(146, 292, 152, 80, fill="blue")

        self.login = tk.Label(self.rightFrame, text="TRA0163", font=font)

        # Render
        self.leftFrame.pack(side=tk.LEFT, fill=tk.Y)

        self.directionFrame.pack(fill=tk.X)
        self.radioButton1.grid(row=0, column=0)
        self.radioButton2.grid(row=0, column=1)

        self.entryFrame.pack(fill=tk.BOTH, expand=tk.TRUE)
        self.inputLabel.pack()
        self.entryInput.pack()
        self.entryInput.focus_force()
        self.outputLabel.pack()
        self.entryOutput.pack()
        self.convertButton.pack(side=tk.BOTTOM)

        self.rightFrame.pack(side=tk.RIGHT)

        self.canvas.pack()
        self.login.pack()


if __name__ == "__main__":
    tk_root = tk.Tk()
    app = MyApp(tk_root)
    tk_root.mainloop()

