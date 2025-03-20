from functools import wraps
from tkinter import Misc, TclError, ttk
import tkinter
from typing import Type, assert_type

from lib.logger import log
from comps.component_meta import ComponentMeta


class Component(ttk.LabelFrame, metaclass=ComponentMeta):
    parent: Misc
    comp_label: str

    def __init__(self, parent: Misc, label: str = "", show_label = True):
        log.debug(f"INFO: Component base __init__ called for {label}")
        dimensions = (100, 100)
        super().__init__(parent, width=dimensions[0], height=dimensions[1])

        # EMPTY_LABEL = "[comp]"
        EMPTY_LABEL = ""
        self.configure(labelwidget=ttk.Label(self, text=label if label and show_label else EMPTY_LABEL))

        self.comp_label = label
        self.parent = parent

    def render(self):
        pass


    def disable(self):
        """Disables the component's iteraction. Recursively disables its children too."""
        
        log.debug("### DISABLE")

        def _disable(node, depth=0):
            children = node.winfo_children()
            if not children:
                return

            log.debug(depth * "\t", f"children count: {len(children)}")

            for ch in children:
                log.debug(depth * "\t", ch)
                try:
                    ch.configure(state="disabled")
                    if isinstance(ch, Component):
                        ch.disable()
                except TclError:
                    pass
                _disable(ch, depth+1)

        _disable(self)


    def enable(self):
        """Enables the component's iteraction. Recursively enables its children too."""

        log.debug("### ENABLE")

        def _enable(node, depth=0):
            children = node.winfo_children()
            if not children:
                return

            log.debug(depth * "\t", f"children count: {len(children)}")

            for ch in children:
                log.debug(depth * "\t", ch)
                try:
                    if isinstance(ch, tkinter.Text):
                        ch.configure(state="normal")
                    else:
                        ch.configure(state="enabled")

                    if isinstance(ch, Component):
                        ch.enable()

                except TclError:
                    pass
                _enable(ch, depth+1)

        _enable(self)


# class A(Component):
#     pass
#
# class B(Component):
#     pass
#
# class C(B):
#     pass
#
# print(A.__name__)
# print(B.__name__)
# print(C.__name__)
# exit(0)


