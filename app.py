from flask import Flask, render_template, request, flash, redirect, session, url_for
from flask_mysqldb import MySQL
import datetime

app = Flask(__name__)
app.secret_key = "matper"
app.config['MYSQL_HOST'] = '138.41.20.102'
app.config['MYSQL_PORT'] = 53306
app.config['MYSQL_USER'] = '5di'
app.config['MYSQL_PASSWORD'] = 'colazzo'
app.config['MYSQL_DB'] = 'termite_calabrese_hyka'

mysql = MySQL(app)

@app.route("/")
def biblioteca():
    ordinamento = request.args.get("ordinamento", "Titolo")
    categoria_selezionata = request.args.get("categoria", "Tutti")

    # Recupero le categorie disponibili
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT DISTINCT Categoria FROM Libri")
    categorie = [row[0] for row in cursor.fetchall()]
    categorie.insert(0, "Tutti")  # Aggiungo l'opzione per visualizzare tutti i libri

    # Costruisco la query principale con filtro categoria
    query = "SELECT * FROM Libri"
    params = []
    if categoria_selezionata != "Tutti":
        query += " WHERE Categoria = %s"
        params.append(categoria_selezionata)

    # Aggiungo l'ordinamento
    if ordinamento == "Autore":
        query += " ORDER BY CodAutore"
    else:
        query += " ORDER BY Titolo"

    cursor.execute(query, params)
    listaLibri = cursor.fetchall()

    return render_template("biblioteca.html", libri=listaLibri, ordinamento=ordinamento, categorie=categorie, categoria_selezionata=categoria_selezionata)

@app.route("/libri")
def libri():
    ordinamento = request.args.get("ordinamento", "Titolo")
    categoria_selezionata = request.args.get("categoria", "Tutti")

    # Recupero le categorie disponibili
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT DISTINCT Categoria FROM Libri")
    categorie = [row[0] for row in cursor.fetchall()]
    categorie.insert(0, "Tutti")  # Aggiungo l'opzione per visualizzare tutti i libri

    # Costruisco la query principale con filtro categoria
    query = "SELECT * FROM Libri"
    params = []
    if categoria_selezionata != "Tutti":
        query += " WHERE Categoria = %s"
        params.append(categoria_selezionata)

    # Aggiungo l'ordinamento
    if ordinamento == "Autore":
        query += " ORDER BY CodAutore"
    else:
        query += " ORDER BY Titolo"

    cursor.execute(query, params)
    listaLibri = cursor.fetchall()

    return render_template("libri.html", libri=listaLibri, ordinamento=ordinamento, categorie=categorie, categoria_selezionata=categoria_selezionata)


@app.route("/gestioneBiblioteca", methods=["GET", "POST"])
def gestioneBiblioteca():


app.run(debug=true)
