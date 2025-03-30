from flask import Flask, render_template, url_for
from MySQL import MYSQL_DB

app = Flask(__name__)

@app.route("/")
def biblioteca():
    return render_template("biblioteca.html")


app.run(debug=True)