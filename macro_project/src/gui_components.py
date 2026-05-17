
"""
*******************************
Author:
u3324971 u3334568 
Assessment 3 
part 3
17/ 05/2026
Programming:
*******************************
"""

from tkinter import (
    Label, 
    Button, 
    Frame, 
    filedialog, 
    OptionMenu, 
    StringVar, 
    Checkbutton, 
    IntVar,
    Canvas,
    Event,
    Widget
    )
from tkinter import ttk
from typing import Self, Any, Callable
from PIL import Image, ImageTk
from pathlib import Path
from math import ceil
from config import SUPPORTED_EXTENSIONS, RAW_DATA_DIR #type: ignore
from shutil import copy

class ImageLabel(Label):
    """this is a class for images. it is a Label so that it can support multiple image file types
    """
    def __init__(self, *args : Any, **kwargs : Any):
        """initialise the gui components"""

        super().__init__(*args, **kwargs)

        #prevents garbage collection messing up the whole thing:
        self.root_image_data = None
        self.image_data = None
        self.image_render = None
        self.grid_propagate(False)

    def grid(self, *args : Any, **kwargs : Any) -> Self:
        """adds a grid to the interface, whilst returning itself to allow the chaining of methods more efficiently"""

        super().grid(*args, **kwargs)
        return self #so that we can chain the methods and i dont have to have a bunch of extra lines to grid
    
    def set_image(self, image: Path, height: int | None = None, width: int | None = None):
        """shows the inputted in the gui"""

        #image_data and image_render are used from pillow to help for all image types
        #currently all images should be png, but its future proofing
        self.root_image_data = Image.open(image)
        self.image_data = self.root_image_data.copy()

        self.resize(height= height, width= width)
        self.image_render = ImageTk.PhotoImage(self.image_data)
        self.configure(image=self.image_render, anchor="center")
        
        #self.bind("<Configure>", self.auto_resize) #removed due to being broken


    def auto_resize(self, event : Event) -> None:
        """resizes the interface to the event size, reporting said size afterwards"""
        self.resize(event.width, event.height)
        print(event.width, event.height)
        
    
    def resize(self, height: int | None = None, width: int | None = None) -> None:
        """resizes the interface to the given size"""

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
    """this class handles the dropdown section of the interface"""

    def __init__(self, root : Widget, text : str="drop down",*args : Any, **kwargs : Any) -> None:
        """initialises the dropdown"""

        self.container = Frame(root)
        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(1)
        super().__init__(master = self.container, *args, **kwargs)
        self.config(background="grey")
        self.columnconfigure(0, weight=1)
        self.header = Button(self.container, text=text, command=self.header_press, background="yellow")
        self.header.grid(row=0, column=0, sticky="nsew")
        self.state_expanded : bool = False

    def open(self) -> None:
        """opens the inputted dropdown"""

        Frame.grid(self, row=1, column=0, sticky="nsew")

    def close(self)-> None:
        """closes the inputted dropdown"""

        Frame.grid_forget(self)

    def cont_grid(self, *args : Any, **kwargs : Any) -> Self:
        """creates a container grid"""

        self.container.grid(*args, **kwargs)
        return self
    
    def cont_grid_forget(self, *args : Any, **kwargs : Any) -> Self:
        """removes a container grid"""

        self.container.grid_forget(*args, **kwargs)
        return self
    
    def header_press(self) -> None:
        """toggles the header state"""

        if not self.state_expanded:
            self.open()
            self.state_expanded = True
        else:
            self.close()
            self.state_expanded = False



class FileChoiceButton(Button):
    """this class contains the file selection button"""

    def __init__(self, root : Widget, after_command : Callable[[], Any] | None = None,*args : Any, **kwargs : Any):
        """initialises the button"""

        super().__init__(root, *args, **kwargs)
        self.config(text="upload file")
        self.config(command=self.onlick)
        self.selected_file = None
        self.after_command = after_command

    def onlick(self) -> None:
        """triggers the upload of a file when the button is clicked"""

        self.selected_file = self.upload_file()
        if self.after_command:
            self.after_command()
    
    def grid(self, **kwargs : Any) -> Self:
        """creates a grid"""

        super().grid(**kwargs)
        return self
    
    def get_file_fir(self) -> str | None:
        """returns the selected file"""

        return self.selected_file
    
    def upload_file(self) -> str:
        """opens a file dialog and returns the selected file's path"""

        file_path = filedialog.askopenfilename()#filetypes=SUPPORTED_EXTENSIONS)
        if file_path:
            print(f"Selected file: {file_path}")
        return file_path


class FolderSelect(OptionMenu):
    """this class handles the folder menu"""

    def __init__(self, root : Widget,*args : Any, **kwargs : Any):
        """initialises the menu"""
        
        self.folders = []
        self.find_folders()
        self.current_value = StringVar(root)
        self.current_value.set(self.folders[0])
        super().__init__(root, self.current_value, *self.folders, *args, **kwargs)

    def find_folders(self) -> None:
        """finds all the folders in the current directory"""

        path = RAW_DATA_DIR/"stream_macroinvertebrates"
        self.folders = [f.name for f in path.iterdir() if f.is_dir()]

    def grid(self, **kwargs : Any) -> Self:
        """creates a grid"""

        super().grid(**kwargs)
        return self

class MoveFileButton(Button):
    """this class handles the move file button"""

    def __init__(self,root : Widget,  file_choice: FileChoiceButton, folder_select:FolderSelect,*args : Any, **kwargs : Any):
        """initialises the button"""

        super().__init__(root, *args, **kwargs)
        self.config(command=self.onclick, text="upload")
        self.file_choice = file_choice
        self.folder_select = folder_select

    def onclick(self):
        """selects a file when the button is clicked"""

        if self.file_choice.selected_file: #only triggers if a file has been selected
            copy(self.file_choice.selected_file, RAW_DATA_DIR/"stream_macroinvertebrates"/self.folder_select.current_value.get())
            print(self.folder_select.current_value.get())

    def grid(self, **kwargs : Any) -> Self:
        """creates a grid"""

        super().grid(**kwargs)
        return self
    
class ClassSelect(Frame):
    """this class handles the selection of data category classes to display analysis for"""

    def __init__(self, *args : Any, **kwargs : Any):
        """sets up the selection interface"""

        super().__init__(*args, **kwargs)
        self.all_checked = IntVar(self)
        self.all_checked_button = Checkbutton(self, variable=self.all_checked, text="all", command=self.toggle_all)
        self.inputs: dict[str, tuple[Checkbutton, IntVar]] = {}
    
    def clear(self) -> None:
        """clears the selected choices"""

        for i in self.inputs.values():
            i[0].destroy()
        self.inputs = {}
        self.all_checked.set(0)
        self.all_checked_button.grid_forget()
        return
    
    def generate_manual(self, folders: list[str]|list[Path]) -> None:
        """collects the datasets of the selected classes"""

        self.clear()
        self.all_checked_button.grid(row=0, column=0, sticky="w")
        self.all_checked.set(1)
        for i in folders:
            var = IntVar(self,1)
            self.inputs[str(i)] = (Checkbutton(self, text=str(i), variable=var, command=self.update_all_checked_passive), var)
        for index, value in enumerate(self.inputs.values()):
            value[0].grid(row = 1+index, column=0, sticky="w")

    def generate_auto_dir(self) -> None:
        """collects the paths to the folders of the selected classes"""

        path = RAW_DATA_DIR/"stream_macroinvertebrates"
        folders = [f.name for f in path.iterdir() if f.is_dir()]
        self.generate_manual(folders)

    def update_all_checked_passive(self) -> None:
        """updates the state of the 'all' selection option"""

        for i in self.inputs.values():
            if i[1].get() == 0:
                self.all_checked.set(0)
                return
        self.all_checked.set(1)

    def toggle_all(self) -> None:
        """toggles all the selection options based on the 'all' selection status"""

        checked = self.all_checked.get()
        for i in self.inputs.values():
            i[1].set(checked)

    def get(self) -> list[str]:
        """returns the selected classes"""

        final = []
        for k, v in self.inputs.items():
            if v[1].get()==1:
                final.append(k)
        return final
    
class ScrollFrame(Frame):
    """this is a class for scroll bar, which enables the viewing of all eda data if it doesn't fit in the window"""

    def __init__(self, *args : Any, **kwargs : Any):
        """initialises the scroll bar"""

        super().__init__(*args, **kwargs)
        self.rowconfigure(0, weight=1)
        self.canvas = Canvas(self)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scroll_bar = ttk.Scrollbar(self)
        self.scroll_bar.grid(row=0, column=1, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.canvas.configure(yscrollcommand=self.scroll_bar.set)

        self.main_frame = Frame(self.canvas)
        self.main_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")

        def _on_mousewheel(event : Event):
            """scrolls the interface when triggered by the mousewheel"""

            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)