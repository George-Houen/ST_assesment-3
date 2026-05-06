import tkinter as tk
import config


root = tk.Tk()
root.title("program")
root.resizable(True, True)
root.minsize(300, 400)
root.state("normal")
root.geometry("300x400")
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

header = tk.Frame(root)
header.grid(row=0, column=0, sticky="ew")
body = tk.Frame(root)
body.grid(row=1, column=0, sticky="ew")
footer = tk.Frame(root)
footer.grid(row=2, column=0, sticky="ew")

#header
header.config(relief="raised", border=2)

tk.Label(header, text="Program", font=("Helvetica", 16, "bold italic")).grid(row=0, column=0)



#footer 
footer.config(relief="raised", border=2)
footer.columnconfigure(1, weight=1)

tk.Label(footer, text="u3324971").grid(row=0, column=0)
tk.Label(footer, text="uxxxxxxx").grid(row=1, column=0)
tk.Button(footer, text="appendix").grid(row=0, column=1, sticky="e") # TODO: currently doesnt have any function to it

#body
body.config()



root.mainloop()