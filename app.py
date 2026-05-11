from flask import Flask, render_template, request, url_for, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "loti_slepena_atslega" # Nepieciešams sesiju darbībai

DATABASE = "To-Do List.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def sakums():
    return render_template("base.html")

@app.route("/pieteikties", methods=['GET', 'POST'])
def pieteikties():
    if request.method == 'POST':
        lietotajs = request.form.get("lietotajs")
        parole = request.form.get("parole")

        conn = sqlite3.connect("To-Do List.db")
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        # Šeit svarīgi: lietotajvards = ?
        c.execute("SELECT * FROM lietotaji WHERE lietotajvards = ?", (lietotajs,))
        atbilde = c.fetchone()
        conn.close()

        if atbilde and check_password_hash(atbilde["parole"], parole):
            session["id"] = atbilde["id"]
            session["lietotajs"] = atbilde["lietotajvards"]
            return redirect("/kalendars")
        else:
            return "Nepareizi dati!"
    return render_template("pieteikties.html")

@app.route("/registreties", methods=['GET', 'POST'])
def registreties():
    if request.method == 'POST':
        lietotajs = request.form.get("lietotajs")
        vards = request.form.get("vards")
        parole = request.form.get("parole")
        
        # Paroles šifrēšana pirms glabāšanas
        parole_hash = generate_password_hash(parole)

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO lietotaji (lietotajvards, vards, parole)
                VALUES (?, ?, ?)
            """, (lietotajs, vards, parole_hash))
            conn.commit()
        except sqlite3.Error:
            return "Lietotājvārds jau aizņemts!"
        finally:
            conn.close()
        return redirect(url_for("pieteikties"))
    
    return render_template("registreties.html")

@app.route("/kalendars")
def kalendars():
    if "id" not in session:
        return redirect(url_for("pieteikties"))

    conn = get_db_connection()
    darbi = conn.execute("SELECT * FROM darbi").fetchall()
    conn.close()
    return render_template("kalendars.html", darbi=darbi)

@app.route('/pievienot', methods=['POST'])
def pievienot():
    uzdevums = request.form['uzdevums']
    datums = request.form['datums']
    laiks = request.form['laiks']
    statuss = request.form.get('statuss', 'Nav sākts')

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO darbi (uzdevums, datums, laiks, statuss)
        VALUES (?, ?, ?, ?)
    ''', (uzdevums, datums, laiks, statuss))
    conn.commit()
    conn.close()
    return redirect(url_for('kalendars'))

if __name__ == "__main__":
    app.run(debug=True)