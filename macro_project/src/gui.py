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

        self.header = tk.Frame(self)
        self.header.grid(row=0, column=0, sticky="nsew")
        self.body = tk.Frame(self)
        self.body.grid(row=1, column=0, sticky="nsew")
        self.footer = tk.Frame(self)
        self.footer.grid(row=2, column=0, sticky="nsew")

        #header
        self.header.config(relief="raised", border=2)
        self.header.columnconfigure(1, weight=1)

        tk.Label(self.header, text="Program", font=("Helvetica", 16, "bold italic")).grid(row=0, column=0)

        self.nav_file_manager = tk.Button(self.header, text="manage files", command=lambda:self.switch_active_page(self.page_file_manager))
        self.nav_2 = tk.Button(self.header, text="EDA", command=lambda:self.switch_active_page(self.page_2))
        self.nav_3 = tk.Button(self.header, text="prediction", command=lambda:self.switch_active_page(self.page_3))

        self.nav_file_manager.grid(row=0, column=2)
        self.nav_2.grid(row=0, column=3)
        self.nav_3.grid(row=0, column=4, sticky="e")

        #footer 
        self.footer.config(relief="raised", border=2)
        self.footer.columnconfigure(1, weight=1)

        tk.Label(self.footer, text="u3324971").grid(row=0, column=0)
        tk.Label(self.footer, text="uxxxxxxx").grid(row=1, column=0)
        tk.Button(self.footer, text="appendix").grid(row=0, column=1, sticky="e") # TODO: currently doesnt have any function to it

        #body
        self.body.config()


        self.page_file_manager = tk.Frame(self.body, background="green", border=2)
        self.page_2 = tk.Frame(self.body, bg="blue")
        self.page_3 = tk.Frame(self.body, background="red")

        #this crap below is weird because i wanted to unpack multiple at once without a stupid if else stack
        self.pages : list[tk.Frame] = [
            self.page_file_manager,
            self.page_2,
            self.page_3
        ]

        tk.Label(self.page_file_manager, text="test").pack()




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



if __name__ == "__main__":
    App().mainloop()