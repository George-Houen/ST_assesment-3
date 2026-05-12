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
        self.geometry("500x400")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.header = tk.Frame(self)
        self.header.grid(row=0, column=0, sticky="nsew")
        self.body = tk.Frame(self)
        self.body.grid(row=1, column=0, sticky="nsew")
        self.footer = tk.Frame(self)
        self.footer.grid(row=2, column=0, sticky="nsew")

        #header
        self.header.config(relief="raised", border=2)
        self.header.columnconfigure(1, weight=1)

        tk.Label(self.header, text="Macro project", font=("Helvetica", 16, "bold italic")).grid(row=0, column=0)

        self.nav_file_manager = tk.Button(self.header, text="manage files", command=lambda:self.switch_active_page(self.page_file_manager))
        self.nav_2 = tk.Button(self.header, text="EDA", command=lambda:self.switch_active_page(self.page_eda))
        self.nav_3 = tk.Button(self.header, text="prediction", command=lambda:self.switch_active_page(self.page_3))

        self.nav_file_manager.grid(row=0, column=2)
        self.nav_2.grid(row=0, column=3)
        self.nav_3.grid(row=0, column=4, sticky="e")

        #footer 
        self.footer.config(relief="raised", border=2)
        self.footer.columnconfigure(1, weight=1)

        tk.Label(self.footer, text="u3324971").grid(row=0, column=0)
        tk.Label(self.footer, text="u3334568").grid(row=1, column=0)
        tk.Button(self.footer, text="appendix").grid(row=0, column=1, sticky="e") # TODO: currently doesnt have any function to it

        #body
        self.body.config()


        self.page_file_manager = tk.Frame(self.body, border=2)
        self.page_eda = tk.Frame(self.body)
        self.page_3 = tk.Frame(self.body, background="red")

        #this crap below is weird because i wanted to unpack multiple at once without a stupid if else stack
        self.pages : list[tk.Frame] = [
            self.page_file_manager,
            self.page_eda,
            self.page_3
        ]
        self.switch_active_page(self.page_file_manager) #set as default


        #EDA page

        self.page_eda.configure()
        self.page_eda.columnconfigure([0,1], weight=1, uniform="equal_cols")
        self.page_eda.rowconfigure(1, minsize=3)
        self.eda_refresh_button = tk.Button(self.page_eda, text="refresh", command=self.run_eda)
        self.eda_refresh_button.grid(column=0, row=0, sticky="ew")
        self.indexer = DatasetIndexer()

        self.indexer_counter = tk.StringVar(value="dataset has not been indexed")
        self.index_count_label = tk.Label(self.page_eda, textvariable=self.indexer_counter)
        self.index_count_label.grid(column=1, row=0, sticky="ew")

        self.data_frame: DataFrame | None

        self.summery_box = tk.Frame(self.page_eda, padx=3, pady=3, border=2, relief="sunken")
        self.summery_box.grid(column=0, columnspan=2, row=1, padx=3, pady=3, sticky="ns")
        self.summery_box.columnconfigure([0,1], weight=1)

        self.eda_class_drop_down = DropDown(self.page_eda,"class distrobution").cont_grid(column = 0, row = 2, columnspan=2, sticky = "ew")
        self.eda_size_drop_down = DropDown(self.page_eda,"size distrobution").cont_grid(column = 0, row = 3, columnspan=2, sticky = "ew")

        self.eda_class_distrobution_image = ImageLabel(self.eda_class_drop_down).grid(column = 0, row = 0, sticky="")
        self.eda_size_distrobution_image = ImageLabel(self.eda_size_drop_down).grid(column = 0, row = 0, sticky="")


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


    def display_eda_summery(self, results : dict[str, float]) -> None:
        for child in self.summery_box.winfo_children():
            child.destroy()
        i = 0
        for k,v in results.items():
            tk.Label(self.summery_box, text=k).grid(row=i, column=0)
            tk.Label(self.summery_box, text=round(v, 2)).grid(row=i, column=2)
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

    def run_eda(self):
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
        pass

    def finished_indexing(self):
        print("finished indexing")
        self.data_frame = self.indexer.output
        if type(self.data_frame) != DataFrame:
            print(type(self.data_frame))
            raise TypeError
        self.eda_service = EDAService(self.data_frame, config.EDA_OUTPUT_DIR)
        eda_summery = self.eda_service.build_summary()
        self.display_eda_summery(eda_summery)
        EDA_IMAGE_SIZE = {"width": 500, "height": None}
        self.eda_class_distrobution_image.set_image(self.eda_service.save_class_distribution(), **EDA_IMAGE_SIZE)
        self.eda_size_distrobution_image.set_image(self.eda_service.save_image_size_distribution(), **EDA_IMAGE_SIZE)
        pass


if __name__ == "__main__":
    App().mainloop()