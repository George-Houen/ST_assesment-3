from tkinter import Label
from typing import Self
from PIL import Image, ImageTk
from pathlib import Path

class ImageLabel(Label):
    """this is a class for images. it is a Label so that it can support multiple image file types
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def grid(self, *args, **kwargs) -> Self:
        super().grid(*args, **kwargs)
        return self #so that we can chain the methods and i dont have to have a bunch of extra lines to grid
    def set_image(self, image: Path):
        #image_data and image_render are used from pillow to help for all image types
        #currently all images should be png, but its future proofing
        image_data = Image.open(image) 
        image_render = ImageTk.PhotoImage(image_data)
        self.configure(image=image_render)