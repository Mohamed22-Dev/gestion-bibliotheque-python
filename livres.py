from tkinter import *
from tkinter import ttk, messagebox
import sqlite3


class LivresFrame(Frame):
    def __init__(self, master):
        super().__init__(master, bg="#F2F2F2")

        Label(
            self,
            text="Gestion des livres",
            font=("Arial", 18, "bold"),
            bg="#F2F2F2"
        ).pack(pady=10)

        form = Frame(self, bg="#FFFFFF", bd=1, relief=SOLID)
        form.pack(fill=X, padx=10, pady=10)

        self.titre = Entry(form)
        self.auteur = Entry(form)
        self.genre = Entry(form)
        self.annee = Entry(form)
        self.quantite = Entry(form)

        labels = ["Titre", "Auteur", "Genre", "Année", "Quantité"]
        entries = [
            self.titre,
            self.auteur,
            self.genre,
            self.annee,
            self.quantite
        ]

        for i in range(len(labels)):
            Label(
                form,
                text=labels[i],
                bg="#FFFFFF"
            ).grid(row=i, column=0, padx=10, pady=5)

            entries[i].grid(row=i, column=1, padx=10, pady=5)

        # Buttons
        Button(
            form,
            text="Ajouter",
            bg="#2E86C1",
            fg="white",
            command=self.ajouter
        ).grid(row=5, column=0, pady=10)

        Button(
            form,
            text="Modifier",
            bg="orange",
            fg="white",
            command=self.modifier
        ).grid(row=5, column=1)

        Button(
            form,
            text="Supprimer",
            bg="#C0392B",
            fg="white",
            command=self.supprimer
        ).grid(row=5, column=2)

        # Recherche
        Label(
            form,
            text="Recherche",
            bg="#FFFFFF"
        ).grid(row=6, column=0, pady=10)

        self.recherche = Entry(form)
        self.recherche.grid(row=6, column=1)

        Button(
            form,
            text="Chercher",
            command=self.chercher
        ).grid(row=6, column=2)

        # Table
        self.table = ttk.Treeview(
            self,
            columns=("id", "titre", "auteur", "genre", "annee", "quantite"),
            show="headings"
        )

        for col in self.table["columns"]:
            self.table.heading(col, text=col.capitalize())

        self.table.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Click event
        self.table.bind("<<TreeviewSelect>>", self.selectionner)

        self.afficher()

    def connect(self):
        return sqlite3.connect("bibliotheque.db")

    def afficher(self):
        for row in self.table.get_children():
            self.table.delete(row)

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM livres")

        for row in cursor.fetchall():
            self.table.insert("", END, values=row)

        conn.close()

    def ajouter(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO livres(titre, auteur, genre, annee, quantite)
        VALUES (?, ?, ?, ?, ?)
        """, (
            self.titre.get(),
            self.auteur.get(),
            self.genre.get(),
            self.annee.get(),
            self.quantite.get()
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo("Succès", "Livre ajouté")

        self.vider()
        self.afficher()

    def modifier(self):
        selected = self.table.focus()

        if not selected:
            return

        data = self.table.item(selected)
        livre_id = data["values"][0]

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE livres
        SET titre=?, auteur=?, genre=?, annee=?, quantite=?
        WHERE id=?
        """, (
            self.titre.get(),
            self.auteur.get(),
            self.genre.get(),
            self.annee.get(),
            self.quantite.get(),
            livre_id
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo("Succès", "Livre modifié")

        self.vider()
        self.afficher()

    def supprimer(self):
        selected = self.table.focus()

        if not selected:
            return

        confirmation = messagebox.askyesno(
            "Confirmation",
            "Voulez-vous supprimer ce livre ?"
        )

        if not confirmation:
            return

        data = self.table.item(selected)
        livre_id = data["values"][0]

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM livres WHERE id=?",
            (livre_id,)
        )

        conn.commit()
        conn.close()

        messagebox.showinfo("Succès", "Livre supprimé")

        self.vider()
        self.afficher()

    def chercher(self):
        mot = self.recherche.get()

        for row in self.table.get_children():
            self.table.delete(row)

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM livres
        WHERE titre LIKE ? OR auteur LIKE ?
        """, (
            f"%{mot}%",
            f"%{mot}%"
        ))

        for row in cursor.fetchall():
            self.table.insert("", END, values=row)

        conn.close()

    def selectionner(self, event):
        selected = self.table.focus()

        if not selected:
            return

        data = self.table.item(selected)
        values = data["values"]

        self.vider()

        self.titre.insert(0, values[1])
        self.auteur.insert(0, values[2])
        self.genre.insert(0, values[3])
        self.annee.insert(0, values[4])
        self.quantite.insert(0, values[5])

    def vider(self):
        self.titre.delete(0, END)
        self.auteur.delete(0, END)
        self.genre.delete(0, END)
        self.annee.delete(0, END)
        self.quantite.delete(0, END)