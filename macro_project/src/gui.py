import tkinter as tk
import config
from pathlib import Path


class App(tk.Tk):
    """Desktop GUI app to interface with microinvertabrate tools"""
    def __init__(self) -> None:
        super().__init__()

        self.title("program")
        self.resizable(True, True)
        self.minsize(500, 400)
        self.state("normal")
        self.geometry("500x400")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        header = tk.Frame(self)
        header.grid(row=0, column=0, sticky="ew")
        body = tk.Frame(self)
        body.grid(row=1, column=0, sticky="ew")
        footer = tk.Frame(self)
        footer.grid(row=2, column=0, sticky="ew")

        #header
        header.config(relief="raised", border=2)
        header.columnconfigure(1, weight=1)

        tk.Label(header, text="Program", font=("Helvetica", 16, "bold italic")).grid(row=0, column=0)

        nav_file_manager = tk.Button(header, text="manage files")
        nav_2 = tk.Button(header, text="EDA")
        nav_3 = tk.Button(header, text="prediction")

        nav_file_manager.grid(row=0, column=2)
        nav_2.grid(row=0, column=3)
        nav_3.grid(row=0, column=4, sticky="e")

        #footer 
        footer.config(relief="raised", border=2)
        footer.columnconfigure(1, weight=1)

        tk.Label(footer, text="u3324971").grid(row=0, column=0)
        tk.Label(footer, text="uxxxxxxx").grid(row=1, column=0)
        tk.Button(footer, text="appendix").grid(row=0, column=1, sticky="e") # TODO: currently doesnt have any function to it

        #body
        body.config()



        self.mainloop()

if __name__ == "__main__":
    App().mainloop