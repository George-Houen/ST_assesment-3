from tkinter import (Label, Button, Frame, filedialog, OptionMenu, StringVar, Checkbutton, IntVar)
from typing import Self
from PIL import Image, ImageTk
from pathlib import Path
from math import ceil
from config import SUPPORTED_EXTENSIONS, RAW_DATA_DIR
from shutil import copy

class ImageLabel(Label):
    """this is a class for images. it is a Label so that it can support multiple image file types
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #prevents garbage collection fucking up the whole thing:
        self.root_image_data = None
        self.image_data = None
        self.image_render = None
        self.grid_propagate(False)
    def grid(self, *args, **kwargs) -> Self:
        super().grid(*args, **kwargs)
        return self #so that we can chain the methods and i dont have to have a bunch of extra lines to grid
    def set_image(self, image: Path, height: int | None = None, width: int | None = None):
        #image_data and image_render are used from pillow to help for all image types
        #currently all images should be png, but its future proofing
        self.root_image_data = Image.open(image)
        self.image_data = self.root_image_data.copy()

        self.resize(height= height, width= width)
        self.image_render = ImageTk.PhotoImage(self.image_data)
        self.configure(image=self.image_render)
        """ removing cos it is so freaking broken
        self.bind("<Configure>", self.auto_resize)
        """


    def auto_resize(self, event):
        self.resize(event.width, event.height)
        print(event.width, event.height)
        
    
    def resize(self, height: int | None = None, width: int | None = None):
        if self.root_image_data:
            w_over_h_ratio = self.root_image_data.width / self.root_image_data.height
            if width and height:
                self.image_data = self.root_image_data.resize((width, height), Image.Resampling.LANCZOS)
            elif width:
                print(width, ceil(w_over_h_ratio/width), w_over_h_ratio)
                self.image_data = self.root_image_data.resize((width, ceil(width/w_over_h_ratio)), Image.Resampling.LANCZOS)
            elif height:
                self.image_data = self.root_image_data.resize((ceil(w_over_h_ratio*height), height), Image.Resampling.LANCZOS)
            else:
                self.image_data = self.root_image_data.copy()

            self.image_render = ImageTk.PhotoImage(self.image_data)
            self.configure(image=self.image_render) # i dont know if this has to be done, but just to be safe
            



class DropDown(Frame):
    def __init__(self, root, text="drop down", *args, **kwargs):
        self.container = Frame(root)
        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(1, minsize=10)
        super().__init__(master = self.container, *args, **kwargs)
        self.config(background="grey")
        self.columnconfigure(0, weight=0)
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



class FileChoiceButton(Button):
    def __init__(self, root, after_command = None, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.config(text="upload file")
        self.config(command=self.onlick)
        self.selected_file = None
        self.after_command = after_command

    def onlick(self):
        self.selected_file = self.upload_file()
        if self.after_command:
            self.after_command()
    
    def grid(self, **kwargs) -> Self:
        super().grid(**kwargs)
        return self
    
    def get_file_fir(self):
        return self.selected_file
    
    def upload_file(self):
        # Opens a file dialog and returns the selected file's path
        file_path = filedialog.askopenfilename()#filetypes=SUPPORTED_EXTENSIONS)
        if file_path:
            print(f"Selected file: {file_path}")
        return file_path


class FolderSelect(OptionMenu):
    def __init__(self, root, *args, **kwargs):
        self.folders = []
        self.find_folders()
        self.current_value = StringVar(root)
        self.current_value.set(self.folders[0])
        super().__init__(root, self.current_value, *self.folders, *args, **kwargs)

    def find_folders(self):
        path = RAW_DATA_DIR/"stream_macroinvertebrates"
        self.folders = [f.name for f in path.iterdir() if f.is_dir()]

    def grid(self, **kwargs) -> Self:
        super().grid(**kwargs)
        return self

class MoveFileButton(Button):
    def __init__(self,root,  file_choice: FileChoiceButton, folder_select:FolderSelect, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.config(command=self.onclick, text="upload")
        self.file_choice = file_choice
        self.folder_select = folder_select
    def onclick(self):
        if self.file_choice.selected_file:
            copy(self.file_choice.selected_file, RAW_DATA_DIR/"stream_macroinvertebrates"/self.folder_select.current_value.get())
            print(self.folder_select.current_value.get())
        print("test 2")
    def grid(self, **kwargs) -> Self:
        super().grid(**kwargs)
        return self
    
class ClassSelect(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.all_checked = IntVar(self)
        self.all_checked_button = Checkbutton(self, variable=self.all_checked, text="all")
        self.inputs: dict[str, tuple[Checkbutton, IntVar]] = {}
    
    def clear(self):
        for i in self.inputs.values():
            i[0].destroy()
        self.inputs = {}
        self.all_checked.set(0)
        self.all_checked_button.grid_forget()
        return
    
    def generate_manual(self, folders: list[str]|list[Path]):
        self.clear()
        self.all_checked_button.grid(row=0, column=0)
        self.all_checked.set(1)
        for i in folders:
            var = IntVar(self)
            self.inputs[str(i)] = (Checkbutton(self, text=str(i), variable=var), var)
        for index, value in enumerate(self.inputs.values()):
            value[0].grid(row = 1+index, column=0)

    def generate_auto_dir(self):
        path = RAW_DATA_DIR/"stream_macroinvertebrates"
        folders = [f.name for f in path.iterdir() if f.is_dir()]
        self.generate_manual(folders)