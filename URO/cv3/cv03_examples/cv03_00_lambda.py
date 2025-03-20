# ------------------------------------------------------------------------------#
# lambda                                                            #
# ------------------------------------------------------------------------------#
import tkinter as tk


class MyApp:
    def __init__(self, window):
        self.l = tk.Label(text="Choose your name:").pack(padx=10, pady=10)

        self.value = tk.StringVar()
        self.value.set(-1)
        self.rb1 = tk.Radiobutton(
            window,
            text="Pepik",
            variable=self.value,
            value="Pepik",
            command=self.print_choosing,
        ).pack()

        self.rb2 = tk.Radiobutton(
            window,
            text="Anicka",
            variable=self.value,
            value="Anicka",
            command=self.print_choosing,
        ).pack()

        self.b = tk.Button(
            window,
            text="Say Hello using only lambda!",
            command=lambda: print("Hello from lamda!"),
        ).pack(padx=10)

        self.b1 = tk.Button(
            window,
            text="Say Hello using my function!",
            command=lambda: self.print_hello("World"),
        ).pack(padx=10)

        self.b2 = tk.Button(
            window,
            text="Say Hello to me!",
            command=lambda: self.print_hello(
                ("Anicko" if self.value.get() == "Anicka" else "Pepiku")
            ),
        ).pack(padx=10)

        self.b3 = tk.Button(
            window,
            text="Say Hello to my friend!",
            command=lambda: self.print_hello_friend(self.value.get()),
        ).pack(padx=10)

    def print_choosing(self):
        print(f"You're choosing {self.value.get()}!")

    def print_hello(self, param):
        print(f"Hello {param}!")

    def print_hello_friend(self, param):
        pozdrav = "Pepiku" if param == "Anicka" else "Anicko"
        print(f"Hello friend {pozdrav}!")


root = tk.Tk()
app = MyApp(root)
root.mainloop()
# ------------------------------------------------------------------------------#
