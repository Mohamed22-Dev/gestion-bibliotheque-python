from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta


class EmpruntsFrame(Frame):
    def __init__(self, master):
        super().__init__(master, bg="#F2F2F2")

        Label(self, text="Gestion des emprunts", font=("Arial", 18, "bold"), bg="#F2F2F2").pack(pady=10)

        form = Frame(self, bg="#FFFFFF")
        form.pack(fill=X, padx=10, pady=10)

        self.livre = ttk.Combobox(form)
        self.membre = ttk.Combobox(form)

        Label(form, text="Livre", bg="#FFFFFF").grid(row=0, column=0, padx=10, pady=5)
        self.livre.grid(row=0, column=1, padx=10, pady=5)

        Label(form, text="Membre", bg="#FFFFFF").grid(row=1, column=0, padx=10, pady=5)
        self.membre.grid(row=1, column=1, padx=10, pady=5)

        Button(form, text="Emprunter", bg="#2E86C1", fg="white", command=self.emprunter).grid(row=2, column=0, pady=10)
        Button(form, text="Retour", bg="#C0392B", fg="white", command=self.retour).grid(row=2, column=1)

        self.table = ttk.Treeview(self, columns=("id", "livre", "membre", "date_emp", "retour_prev", "retour"), show="headings")

        for col in self.table["columns"]:
            self.table.heading(col, text=col)

        self.table.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.charger()
        self.afficher()

    def connect(self):
        return sqlite3.connect("bibliotheque.db")

    def charger(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT id, titre FROM livres")
        livres = cursor.fetchall()
        self.livre["values"] = [f"{x[0]} - {x[1]}" for x in livres]

        cursor.execute("SELECT id, nom FROM membres")
        membres = cursor.fetchall()
        self.membre["values"] = [f"{x[0]} - {x[1]}" for x in membres]

        conn.close()

    def afficher(self):
        for row in self.table.get_children():
            self.table.delete(row)

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT emprunts.id, livres.titre, membres.nom,
        date_emprunt, date_retour_prevue, date_retour
        FROM emprunts
        JOIN livres ON livres.id = emprunts.livre_id
        JOIN membres ON membres.id = emprunts.membre_id
        """)

        for row in cursor.fetchall():
            self.table.insert("", END, values=row)

        conn.close()

    def emprunter(self):
        livre_id = self.livre.get().split(" - ")[0]
        membre_id = self.membre.get().split(" - ")[0]

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT quantite FROM livres WHERE id=?", (livre_id,))
        quantite = cursor.fetchone()[0]

        if quantite <= 0:
            messagebox.showerror("Erreur", "Livre indisponible")
            return

        cursor.execute("""
        SELECT * FROM emprunts
        WHERE livre_id=? AND membre_id=? AND date_retour IS NULL
        """, (livre_id, membre_id))

        if cursor.fetchone():
            messagebox.showerror("Erreur", "Livre déjà emprunté")
            return

        date_emp = datetime.now().strftime("%Y-%m-%d")
        retour_prev = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

        cursor.execute("""
        INSERT INTO emprunts(livre_id, membre_id, date_emprunt, date_retour_prevue)
        VALUES (?, ?, ?, ?)
        """, (livre_id, membre_id, date_emp, retour_prev))

        cursor.execute("UPDATE livres SET quantite = quantite - 1 WHERE id=?", (livre_id,))

        conn.commit()
        conn.close()

        messagebox.showinfo("Succès", "Emprunt enregistré")
        self.afficher()

    def retour(self):
        selected = self.table.focus()

        if not selected:
            return

        data = self.table.item(selected)
        emprunt_id = data["values"][0]
        titre = data["values"][1]

        conn = self.connect()
        cursor = conn.cursor()

        date_retour = datetime.now().strftime("%Y-%m-%d")

        cursor.execute("""
        UPDATE emprunts
        SET date_retour=?
        WHERE id=?
        """, (date_retour, emprunt_id))

        cursor.execute("UPDATE livres SET quantite = quantite + 1 WHERE titre=?", (titre,))

        conn.commit()
        conn.close()

        messagebox.showinfo("Succès", "Livre retourné")
        self.afficher()