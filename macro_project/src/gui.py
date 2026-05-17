import tkinter as tk
import config
from pathlib import Path
from threading import * #type: ignore
from services.dataset_indexer import DatasetIndexer
from services.eda_service import EDAService
from pandas import DataFrame
from gui_components import *


class App(tk.Tk):
    """Desktop GUI app to interface with microinvertabrate tools"""
    def __init__(self) -> None:
        super().__init__()

        self.title("Macro project")
        self.resizable(True, True)
        self.minsize(500, 400)
        self.state("normal")
        self.geometry("500x500")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.header = tk.Frame(self)
        self.header.grid(row=0, column=0, sticky="nsew")
        self.body = ScrollFrame(self)
        self.body.grid(row=1, column=0, sticky="nsew")
        self.footer = tk.Frame(self)
        self.footer.grid(row=2, column=0, sticky="nsew")

        #header
        self.header.config(relief="raised", border=2)
        self.header.columnconfigure(1, weight=1)

        tk.Label(self.header, text="Macro project", font=("Helvetica", 16, "bold italic")).grid(row=0, column=0)

        self.nav_file_manager = tk.Button(self.header, text="manage files", command=lambda:self.switch_active_page(self.page_file_manager))
        self.nav_2 = tk.Button(self.header, text="EDA", command=lambda:self.switch_active_page(self.page_eda))

        self.nav_file_manager.grid(row=0, column=2)
        self.nav_2.grid(row=0, column=3)

        #footer 
        self.footer.config(relief="raised", border=2)
        self.footer.columnconfigure(1, weight=1)

        tk.Label(self.footer, text="u3324971").grid(row=0, column=0)
        tk.Label(self.footer, text="u3334568").grid(row=1, column=0)
        tk.Button(self.footer, text="appendix").grid(row=0, column=1, sticky="e") # TODO: currently doesnt have any function to it

        #body
        self.body.config()


        self.page_file_manager = tk.Frame(self.body.main_frame, border=2)
        self.page_eda = tk.Frame(self.body.main_frame)

        #this crap below is weird because i wanted to unpack multiple at once without a stupid if else stack
        self.pages : list[tk.Frame] = [
            self.page_file_manager,
            self.page_eda
        ]
        self.switch_active_page(self.page_file_manager) #set as default


        #EDA page

        self.page_eda.configure()
        self.page_eda.columnconfigure([0,1], weight=1, uniform="equal_cols")
        self.page_eda.rowconfigure(1, minsize=3)
        self.indexing_refresh_button = tk.Button(self.page_eda, text="refresh", command=self.run_indexing)
        self.indexing_refresh_button.grid(column=0, row=0, sticky="ew")
        self.indexer = DatasetIndexer()

        self.indexer_counter = tk.StringVar(value="dataset has not been indexed")
        self.index_count_label = tk.Label(self.page_eda, textvariable=self.indexer_counter)
        self.index_count_label.grid(column=1, row=0, sticky="ew")

        self.data_frame: DataFrame | None = None

        self.summery_box = tk.Frame(self.page_eda, padx=3, pady=3, border=2, relief="sunken")
        self.summery_box.grid(column=0, row=1, padx=3, pady=3, sticky="ns")
        self.summery_box.columnconfigure([0,1], weight=1)
        
        self.class_select = ClassSelect(self.page_eda, padx=3, pady=3, border=2, relief="sunken")
        self.class_select.grid(column=1, row=1, padx=3, pady=3, sticky="ns")

        self.perform_eda_button = Button(self.class_select, command=self.run_eda)
        self.track_eda_counter = tk.StringVar(value="")
        self.track_eda = Label(self.class_select, textvariable=self.track_eda_counter)

        self.eda_output_images = Frame(self.page_eda)
        self.eda_output_images.grid(column = 0, row = 2, columnspan=2, sticky = "nsew")
        self.eda_output_images.columnconfigure((0,1), weight=1)

        #file control page

        self.page_file_manager.config()
        self.file_select = FileChoiceButton(self.page_file_manager).grid(row=1)
        self.folder_select = FolderSelect(self.page_file_manager).grid(row=2)
        self.move_file_button = MoveFileButton(self.page_file_manager, self.file_select, self.folder_select).grid(row=3)
        self.select_image = ImageLabel(self.page_file_manager).grid(row=1, rowspan=3, column = 1)
        self.select_image.resize(width=350)
        self.file_select.after_command= lambda:(
            self.select_image.set_image(Path(self.file_select.selected_file)) #type: ignore
        )


    def display_eda_summery(self, results : dict[str, float | int | str]) -> None:
        for child in self.summery_box.winfo_children():
            child.destroy()
        i = 0
        for k,v in results.items():
            tk.Label(self.summery_box, text=k).grid(row=i, column=0)
            tk.Label(self.summery_box, text=v).grid(row=i, column=2)
            i+=1
        tk.Frame( #vertical culumn serperator
                self.summery_box,
                width=1,
                bg="black"
            ).grid(row=0, column=1, rowspan=i, sticky="ns", padx=5)

    def switch_active_page(self, page: tk.Frame) -> None:
        """changes which page is open in body

        Args:
            page (tk.Frame): which page to open (should be in pages list)
        """
        if page in self.pages:
            for i in self.pages: 
                i.pack_forget()
                print("oops")
            print(f"opening page: {page}")
            page.pack(fill="both", expand=True)
        else:
            raise ValueError("page to be opened should be in body and self.pages")

    def run_indexing(self) -> None:
        print("start indexing")
        thread = Thread(
            target=lambda:self.indexer.build_dataframe(
                lambda:self.after( 2, func = lambda:self.indexer_counter.set(f"{self.indexer.counter} files indexed.")),
                lambda: self.after( 2,
                    self.finished_indexing
                )
            )
        )
        thread.start()
        

    def finished_indexing(self) -> None:
        print("finished indexing")
        self.data_frame = self.indexer.output
        if type(self.data_frame) != DataFrame:
            print(self.data_frame, type(self.data_frame))
            raise TypeError (self.data_frame, type(self.data_frame))
        
        print(self.data_frame.columns.to_list())
        self.class_select.generate_manual(list(self.data_frame["label"])) #type: ignore
        self.perform_eda_button.grid(column=0, sticky="nsew")
        self.track_eda.grid(column=0, sticky="nsew")

        
    
    def run_eda(self) -> None:
        for i in self.eda_output_images.winfo_children():
            i.destroy()
        if type(self.data_frame) != DataFrame:
            print(self.data_frame, type(self.data_frame))
            raise TypeError (self.data_frame, type(self.data_frame))
        
        self.eda_service = EDAService(self.data_frame, config.EDA_OUTPUT_DIR, config.REPORT_OUTPUT_DIR)
        self.eda_service.filter_data_frame(self.class_select.get())

        eda_summery = self.eda_service.build_summary()
        self.display_eda_summery(eda_summery)
    
        thread = Thread(
            target=lambda:self.eda_service.save_all(
                lambda:self.after( 2, func = lambda:self.track_eda_counter.set(f"currently processing: {self.eda_service.track_save_all_progress}")),
                lambda: self.after( 2,
                    self.finished_eda
                )
            )
        )
        thread.start()
    
    def generate_eda_dropdown(self, title : str, path : Path) -> None:
        drop_down_frame = DropDown(self.eda_output_images, title).cont_grid(column = 0, sticky = "ew")
        image = ImageLabel(drop_down_frame).grid(column = 0, row = 0, sticky="ew")
        image.set_image(path, **config.EDA_IMAGE_SIZE)

    def finished_eda(self):
        self.track_eda_counter.set("eda complete")
        image_paths = self.eda_service.output_images
        
        for title, path in image_paths.items():
            self.generate_eda_dropdown(title, path)
            
        


if __name__ == "__main__":
    App().mainloop()