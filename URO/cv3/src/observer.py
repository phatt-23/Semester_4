#!/usr/bin/env python3

from typing import Callable


class Observer:
    def update(self, obervable: "Observable", *args, **kwargs):
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
