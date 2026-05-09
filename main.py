from tkinter import *
from tkinter import ttk

from database import create_tables
from livres import LivresFrame
from membres import MembresFrame
from emprunts import EmpruntsFrame


create_tables()

root = Tk()
root.iconbitmap("logo.ico")
root.title("Bibliothèque")
root.geometry("1200x700")
root.configure(bg="#F2F2F2")

style = ttk.Style()
style.theme_use("clam")

notebook = ttk.Notebook(root)
notebook.pack(fill=BOTH, expand=True)

livres_tab = LivresFrame(notebook)
membres_tab = MembresFrame(notebook)
emprunts_tab = EmpruntsFrame(notebook)

notebook.add(livres_tab, text="Livres")
notebook.add(membres_tab, text="Membres")
notebook.add(emprunts_tab, text="Emprunts")

root.mainloop()