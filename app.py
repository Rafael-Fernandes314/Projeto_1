from flask import Flask, render_template, request, redirect
app = Flask(__name__)

# rotas
@app.route("/cadastro")
def home():
    return render_template("cadastro.html")
@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/inicial")
def inicial():
    return render_template("inicial.html")
@app.route("/criar")
def criar():
    return render_template("criar_lembrete.html")
@app.route("/editar")
def editar():
    return render_template("editar_lembrete.html")