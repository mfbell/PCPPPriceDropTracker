import tkinter as tk
from tkinter import ttk

root = tk.Tk()

s = ttk.Style()
s.map("C.TFrame",
      foreground=[("pressed", "red"), ("active", "blue")],
      background=[("pressed", "!disabled", "black"), ("active", "white")])
s.map("C.TButton",
      foreground=[("pressed", "red"), ("active", "blue")],
      background=[("pressed", "!disabled", "black"), ("active", "white")])
def show():
    print(s.layout("TButton"))
    print(s.layout("C.TButton"))
    root.bell()

def show1(event):
    print(s.layout("TFrame"))
    print(s.layout("C.TFrame"))

frame = ttk.Frame(root, style="C.TFrame")
text = ttk.Label(frame, text="This is some really long text\n123...")
b = ttk.Button(frame, text="show", command=show, style="C.TButton")

frame.bind("<Button-1>", show1)
text.bind("<Button-1>", show1)

frame.grid()
text.grid()
b.grid()

root.mainloop()
