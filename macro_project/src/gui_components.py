from tkinter import Label, Button, Frame
from typing import Self
from PIL import Image, ImageTk
from pathlib import Path

class ImageLabel(Label):
    """this is a class for images. it is a Label so that it can support multiple image file types
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #prevents garbage collection fucking up the whole thing:
        self.image_data = None
        self.image_render = None
    def grid(self, *args, **kwargs) -> Self:
        super().grid(*args, **kwargs)
        return self #so that we can chain the methods and i dont have to have a bunch of extra lines to grid
    def set_image(self, image: Path, size :tuple [int, int]|None = None ):
        #image_data and image_render are used from pillow to help for all image types
        #currently all images should be png, but its future proofing
        self.image_data = Image.open(image) 
        if size:
            self.image_data = self.image_data.resize(size, Image.Resampling.LANCZOS)
        self.image_render = ImageTk.PhotoImage(self.image_data)
        self.configure(image=self.image_render)


class DropDown(Frame):
    def __init__(self, root, text="drop down", *args, **kwargs):
        self.container = Frame(root, background= "teal")
        self.container.columnconfigure(1, weight=1)
        self.container.rowconfigure(1, minsize=10)
        super().__init__(master = self.container, *args, **kwargs)
        self.header = Button(self.container, text=text, command=self.header_press, background="yellow")
        self.header.grid(row=0, column=0, sticky="nsew")
        self.state_expanded : bool = False
    def open(self):
        Frame.grid(self, row=1, column=0, sticky="nsew")
    def close(self):
        Frame.grid_forget(self)
    def cont_grid(self, *args, **kwargs):
        self.container.grid(*args, **kwargs)
        return self
    def cont_grid_forget(self, *args, **kwargs) -> Self:
        self.container.grid_forget(*args, **kwargs)
        return self
    def header_press(self):
        if not self.state_expanded:
            self.open()
            self.state_expanded = True
        else:
            self.close()
            self.state_expanded = False
