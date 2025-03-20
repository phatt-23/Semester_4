from tkinter import font
from typing import Literal


class FontBuilder():
    _sans_family: str
    _mono_family: str
    _unit_size: int
    _weight: Literal["normal", "bold"]
    _monospaced: bool

    def __init__(self):
        self._sans_family = "Iosevka Nerd Font"  #"NotoSans"
        self._mono_family = "FiraCode Nerd Font"
        self._unit_size = 8
        self._weight = "normal"
        self._monospaced = False

    def mono(self):
        self._monospaced = True
        return self

    def sans(self):
        self._monospaced = False
        return self

    def size(self, font_size: Literal["tiny", "small", "normal", "big", "huge"]) -> "FontBuilder":
        match font_size:
            case "tiny":
                self._unit_size = 6
            case "small":
                self._unit_size = 8
            case "normal":
                self._unit_size = 10
            case "big":
                self._unit_size = 12
            case "huge":
                self._unit_size = 14
        return self

    def weight(self, weight: Literal["normal", "bold"]) -> "FontBuilder":
        self._weight = weight
        return self

    def build(self):
        family = self._mono_family if self._monospaced else self._sans_family
        return (family, self._unit_size, self._weight)

    def buildTk(self):
        family = self._mono_family if self._monospaced else self._sans_family
        return font.Font(family=family, size=self._unit_size, weight=self._weight)

