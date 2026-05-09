from tkinter import *
from tkinter import ttk, messagebox
import sqlite3


class MembresFrame(Frame):
    def __init__(self, master):
        super().__init__(master, bg="#F2F2F2")

        Label(
            self,
            text="Gestion des membres",
            font=("Arial", 18, "bold"),
            bg="#F2F2F2"
        ).pack(pady=10)

        form = Frame(self, bg="#FFFFFF")
        form.pack(fill=X, padx=10, pady=10)

        self.nom = Entry(form)
        self.prenom = Entry(form)
        self.email = Entry(form)
        self.adhesion = Entry(form)

        labels = ["Nom", "Prénom", "Email", "Adhésion"]
        entries = [
            self.nom,
            self.prenom,
            self.email,
            self.adhesion
        ]

        for i in range(len(labels)):
            Label(
                form,
                text=labels[i],
                bg="#FFFFFF"
            ).grid(row=i, column=0, padx=10, pady=5)

            entries[i].grid(row=i, column=1, padx=10, pady=5)

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

        self.table = ttk.Treeview(
            self,
            columns=("id", "nom", "prenom", "email", "adhesion"),
            show="headings"
        )

        for col in self.table["columns"]:
            self.table.heading(col, text=col.capitalize())

        self.table.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.table.bind("<<TreeviewSelect>>", self.selectionner)

        self.afficher()

    def connect(self):
        return sqlite3.connect("bibliotheque.db")

    def afficher(self):
        for row in self.table.get_children():
            self.table.delete(row)

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM membres")

        for row in cursor.fetchall():
            self.table.insert("", END, values=row)

        conn.close()

    def ajouter(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO membres(nom, prenom, email, adhesion)
        VALUES (?, ?, ?, ?)
        """, (
            self.nom.get(),
            self.prenom.get(),
            self.email.get(),
            self.adhesion.get()
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo("Succès", "Membre ajouté")

        self.vider()
        self.afficher()

    def modifier(self):
        selected = self.table.focus()

        if not selected:
            return

        data = self.table.item(selected)
        membre_id = data["values"][0]

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE membres
        SET nom=?, prenom=?, email=?, adhesion=?
        WHERE id=?
        """, (
            self.nom.get(),
            self.prenom.get(),
            self.email.get(),
            self.adhesion.get(),
            membre_id
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo("Succès", "Membre modifié")

        self.vider()
        self.afficher()

    def supprimer(self):
        selected = self.table.focus()

        if not selected:
            return

        data = self.table.item(selected)
        membre_id = data["values"][0]

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM membres WHERE id=?",
            (membre_id,)
        )

        conn.commit()
        conn.close()

        messagebox.showinfo("Succès", "Membre supprimé")

        self.vider()
        self.afficher()

    def chercher(self):
        mot = self.recherche.get()

        for row in self.table.get_children():
            self.table.delete(row)

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM membres
        WHERE nom LIKE ? OR adhesion LIKE ?
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

        self.nom.insert(0, values[1])
        self.prenom.insert(0, values[2])
        self.email.insert(0, values[3])
        self.adhesion.insert(0, values[4])

    def vider(self):
        self.nom.delete(0, END)
        self.prenom.delete(0, END)
        self.email.delete(0, END)
        self.adhesion.delete(0, END)