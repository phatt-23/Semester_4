from functools import wraps
from tkinter import Widget, Tk
from typing import Callable


def print_hierarchy(w: Widget | Tk, depth=0):
    print(
        "    " * depth
        + w.winfo_class()
        + " w="
        + str(w.winfo_width())
        + " h="
        + str(w.winfo_height())
        + " x="
        + str(w.winfo_x())
        + " y="
        + str(w.winfo_y())
    )
    for i in w.winfo_children():
        print_hierarchy(i, depth + 1)

def log_call(f: Callable):
    @wraps(f)
    def g(*args, **kwargs):
        print("Called", f.__name__)
        f(*args, **kwargs)
    return g
