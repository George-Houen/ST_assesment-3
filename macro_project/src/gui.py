import tkinter as tk


root = tk.Tk()
root.geometry("300x400")

header = tk.Frame(root)
header.grid(row=0, column=0)
body = tk.Frame(root)
body.grid(row=1, column=0)
body = tk.Frame(root)
body.grid(row=2, column=0)

root.mainloop()