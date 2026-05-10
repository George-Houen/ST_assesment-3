from tkinter import Label
from typing import Self


class ImageLabel(Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def grid(self, *args, **kwargs) -> Self:
        super().grid(*args, **kwargs)
        return self #so that we can chain the methods and i dont have to have a bunch of extra lines to grid