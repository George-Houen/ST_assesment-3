from tkinter import Label
from typing import Self
from PIL import Image, ImageTk
from pathlib import Path

class ImageLabel(Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def grid(self, *args, **kwargs) -> Self:
        super().grid(*args, **kwargs)
        return self #so that we can chain the methods and i dont have to have a bunch of extra lines to grid
    def set_image(self, image: Path):
        image_data = Image.open(image)
        image_render = ImageTk.PhotoImage(image_data)
        self.configure(image=image_render)