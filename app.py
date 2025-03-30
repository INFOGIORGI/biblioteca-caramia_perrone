from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "colazzo"

# MySQL DB config
app.config["MYSQL_USER"] = "5di"
app.config["MYSQL_PASSWORD"] = "colazzo"
app.config["MYSQL_HOST"] = "138.41.20.102"
app.config["MYSQL_PORT"] = 53306
app.config["MYSQL_DB"] = "perrone_caramia"

mysql = MySQL(app)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM Utenti WHERE email = %s", (data["email"],))
        if cursor.fetchone()[0] > 0:
            flash("Email già registrata. Usa un'altra email.", "danger")
            return redirect(url_for("register"))
        cursor.execute("SELECT COUNT(*) FROM Utenti")
        count = cursor.fetchone()[0]
        idUtente = f"U{count + 1:03}"
        hashed_password = generate_password_hash(data["password"])
        query = """
            INSERT INTO Utenti (idUtente, nome, cognome, dataNascita, email, telefono, indirizzo, pswrd)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (idUtente, data["nome"], data["cognome"], data["dataNascita"], data["email"], data["telefono"], data["indirizzo"], hashed_password)
        cursor.execute(query, values)
        mysql.connection.commit()
        flash("Registrazione completata con successo. Effettua il login.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT idUtente, pswrd FROM Utenti WHERE email = %s", (data["email"],))
        user = cursor.fetchone()
        if user and check_password_hash(user[1], data["password"]):
            session["user_id"] = user[0]
            flash("Login effettuato con successo.", "success")
            return redirect(url_for("biblioteca"))
        else:
            flash("Email o password errati. Riprova.", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logout effettuato con successo.", "success")
    return redirect(url_for("login"))

@app.before_request
def require_login():
    allowed_routes = ["login", "register", "static"]
    if (request.endpoint not in allowed_routes) and ("user_id" not in session):
        return redirect(url_for("login"))

@app.route("/")
def biblioteca():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Autori")
    autori = cursor.fetchall()
    cursor.execute("SELECT * FROM Utenti")
    utenti = cursor.fetchall()
    cursor.execute("""
        SELECT Libri.isbn, Libri.titolo, CONCAT(Autori.nome, ' ', Autori.cognome) AS autore, 
               Libri.genere, Libri.annoUscita, Libri.casaEditrice, Libri.noleggio
        FROM Libri
        JOIN Autori ON Libri.idAutore = Autori.idAutore
    """)
    libri = cursor.fetchall()
    return render_template("biblioteca.html", autori=autori, utenti=utenti, libri=libri)

@app.route("/libri", methods=["POST"])
def aggiungi_libro():
    data = request.form
    query = """
        INSERT INTO Libri (isbn, titolo, idAutore, genere, annoUscita, casaEditrice, noleggio)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (data["isbn"], data["titolo"], data["idAutore"], data["genere"], data["annoUscita"], data["casaEditrice"], data["noleggio"] == "true")
    cursor = mysql.connection.cursor()
    cursor.execute(query, values)
    mysql.connection.commit()
    return redirect(url_for("biblioteca"))

@app.route("/autori", methods=["POST"])
def aggiungi_autore():
    data = request.form
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM Autori")
    count = cursor.fetchone()[0]
    idAutore = f"B{count + 1:03}"
    query = """
        INSERT INTO Autori (idAutore, nome, cognome, nazionalità, dataNascita, dataMorte)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (
        idAutore,
        data["nome"],
        data["cognome"],
        data["nazionalita"],
        data["dataNascita"],
        data["dataMorte"] if data.get("dataMorte") else None
    )
    cursor.execute(query, values)
    mysql.connection.commit()
    return redirect(url_for("biblioteca"))

@app.route("/libri/cerca", methods=["GET"])
def cerca_libri():
    query = request.args.get("q", "")
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT Libri.isbn, Libri.titolo, CONCAT(Autori.nome, ' ', Autori.cognome) AS autore, 
               Libri.genere, Libri.annoUscita, Libri.casaEditrice, Libri.noleggio
        FROM Libri
        JOIN Autori ON Libri.idAutore = Autori.idAutore
        WHERE Libri.titolo LIKE %s OR Autori.nome LIKE %s OR Autori.cognome LIKE %s
    """, (f"%{query}%", f"%{query}%", f"%{query}%"))
    libri = cursor.fetchall()
    return render_template("biblioteca.html", libri=libri)

@app.route("/libri", methods=["GET"])
def cerca_e_ordina_libri():
    query = request.args.get("q", "")
    ordine = request.args.get("ordine", "titolo")
    cursor = mysql.connection.cursor()
    cursor.execute(f"""
        SELECT Libri.isbn, Libri.titolo, CONCAT(Autori.nome, ' ', Autori.cognome) AS autore, 
               Libri.genere, Libri.annoUscita, Libri.casaEditrice, Libri.noleggio
        FROM Libri
        JOIN Autori ON Libri.idAutore = Autori.idAutore
        WHERE Libri.titolo LIKE %s OR Autori.nome LIKE %s OR Autori.cognome LIKE %s
        ORDER BY {ordine}
    """, (f"%{query}%", f"%{query}%", f"%{query}%"))
    libri = cursor.fetchall()
    cursor.execute("SELECT * FROM Autori")
    autori = cursor.fetchall()
    cursor.execute("SELECT * FROM Utenti")
    utenti = cursor.fetchall()
    return render_template("biblioteca.html", libri=libri, autori=autori, utenti=utenti, query=query, ordine=ordine)

@app.route("/noleggi", methods=["GET"])
def visualizza_noleggi():
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT Noleggi.idNoleggio, CONCAT(Utenti.nome, ' ', Utenti.cognome) AS utente, 
               Libri.titolo, Noleggi.inizioNoleggio, Noleggi.fineNoleggio, Noleggi.restituzione
        FROM Noleggi
        JOIN Utenti ON Noleggi.idUtente = Utenti.idUtente
        JOIN Libri ON Noleggi.isbn = Libri.isbn
    """)
    noleggi = cursor.fetchall()
    return render_template("noleggi.html", noleggi=noleggi)

@app.route("/noleggi", methods=["POST"])
def aggiungi_noleggio():
    data = request.form
    try:
        cursor = mysql.connection.cursor()

        # Verifica se il libro è già noleggiato
        cursor.execute("SELECT noleggio FROM Libri WHERE isbn = %s and restituzione = TRUE", (data["isbn"],))
        libro = cursor.fetchone()
        if libro and libro[0]:
            flash("Il libro selezionato è già noleggiato.", "danger")
            return redirect(url_for("visualizza_noleggi"))

        cursor.execute("SELECT COUNT(*) FROM Noleggi")
        count = cursor.fetchone()[0]
        idNoleggio = f"N{count + 1:03}"
        query_noleggio = """
            INSERT INTO Noleggi (idNoleggio, idUtente, isbn, inizioNoleggio, fineNoleggio, restituzione)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values_noleggio = (idNoleggio, data["idUtente"], data["isbn"], data["inizioNoleggio"], data["fineNoleggio"], False)
        cursor.execute(query_noleggio, values_noleggio)

        # Aggiorna la disponibilità del libro
        query_libro = "UPDATE Libri SET noleggio = TRUE WHERE isbn = %s"
        cursor.execute(query_libro, (data["isbn"],))

        mysql.connection.commit()
        flash("Noleggio aggiunto con successo.", "success")
        return redirect(url_for("visualizza_noleggi"))
    except Exception as e:
        mysql.connection.rollback() # Rollback in caso di errore
        flash(f"Errore durante l'aggiunta del noleggio: {str(e)}", "danger")
        return redirect(url_for("visualizza_noleggi"))

@app.route("/noleggi/restituisci/<idNoleggio>", methods=["POST"])
def restituisci_noleggio(idNoleggio):
    cursor = mysql.connection.cursor()

    # Recupera l'ISBN del libro associato al noleggio
    cursor.execute("SELECT isbn FROM Noleggi WHERE idNoleggio = %s", (idNoleggio,))
    isbn = cursor.fetchone()[0]

    # Aggiorna il noleggio come restituito
    query_noleggio = """
        UPDATE Noleggi
        SET restituzione = TRUE, dataRestituzione = CURDATE()
        WHERE idNoleggio = %s
    """
    cursor.execute(query_noleggio, (idNoleggio,))

    # Aggiorna la disponibilità del libro
    query_libro = "UPDATE Libri SET noleggio = FALSE WHERE isbn = %s"
    cursor.execute(query_libro, (isbn,))

    mysql.connection.commit()
    flash("Libro restituito con successo.", "success")
    return redirect(url_for("visualizza_noleggi"))

if __name__ == "__main__":
    app.run(debug=True)