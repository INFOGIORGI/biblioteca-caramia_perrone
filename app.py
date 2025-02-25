from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
def biblioteca():
    return render_template("biblioteca.html")


app.run(debug=True)