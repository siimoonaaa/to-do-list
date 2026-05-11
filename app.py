from flask import Flask, render_template, request, url_for, redirect
import sqlite3

app = Flask(__name__)

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
		c.execute("SELECT * FROM lietotaji WHERE username = ?", (lietotajs,))
		atbilde = c.fetchone()
		conn.close()

    if atbilde and check_password_hash(atbilde["parole"], parole):
    	session["id"] = atbilde["id"]
    	session["lietotajs"] = atbilde["username"]
    	session["vards"] = atbilde["vards"]
    	return redirect("/kalendars")
	else:
		return "nepareizi dati!"

return render_template("pieteikties.html")


@app.route("/registreties")
def registreties():
	conn = sqlite3.connect("To-Do list.db")
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	lietotajs = request.form.get("lietotajs")
	vards = request.form.get("vards")
	epasts = request.form.get("epasts")
	parole = request.form.get("parole")
	id = str(uuid.uuid4())
	parole_hash = generate_password_hash(parole)
	insert = """
	INSERT INTO lietotaji (uuid, lietotajs, vards, epasts, parole_hash)
	VALUES (?, ?, ?, ?)
	"""

	users = (id, lietotajs, vards, epasts, parole_hash)
	cursor.execute(insert, data)
	conn.commit()
	conn.close()

	return render_template("registreties.html")

@app.route("/kalendars")
def kalendars():
	conn = sqlite3.connect("To-Do list.db")
	c = conn.cursor()

	c.excute("SELECT * FROM kalendars")
	darbi = c.fetchall()

	conn.close()

	return render_template("kalendars.html", kalendars=kalendars)

@app.route('/pievienot', methods=['POST'])
def pievienot():
	uzdevums = request.form['uzdevums']
	datums = request.form['datums']
	laiks = request.form['laiks']
	statuss = request.form['statuss']

	conn = sqlite3.connect('To-Do List.db')
	c = conn.cursor()

	c.execute('''
	INSERT INTO darbi (uzdevums, datums, laiks, statuss)
	VALUES (?, ?, ?, ?)
	''', (uzdevums, datums, laiks, statuss))

	conn.commit()
	conn.close()

	return redirect('/')



if __name__ == "__main__":
	app.run(debug = True)