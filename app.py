from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
usuarios_cadastrados = []

# rotas
@app.route("/cadastro", methods=["POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        usuarios_cadastrados.append({
            'nome': nome,
            'email': email
        })
        return redirect(url_for("login", mensagem="cadastro_sucesso"))
    return render_template("cadastro.html")

@app.route("/login", methods=["POST"])
def login():
    mensagem = request.args.get('mensagem')
    if request.method == "POST":
        email = request.form.get("email")
        usuario = next((i for i in usuarios_cadastrados if i['email'] == email), None)
        if not usuario:
            return redirect(url_for("login", mensagem="email_nao_encontrado"))

        return redirect(url_for("inicial", nome=usuario['nome']))
    return render_template("login.html", mensagem=mensagem)

@app.route("/inicial")
def inicial():
    nome = request.args.get('nome')
    return render_template("inicial.html", nome=nome)

@app.route("/criar", methods=["GET", "POST"])
def criar():
    if request.method == "POST":
        nome = request.args.get('nome')
        return redirect(url_for("inicial", nome=nome) if nome else url_for("inicial"))
    return render_template("criar_lembrete.html")

@app.route("/editar")
def editar():
    return render_template("editar_lembrete.html")

@app.route("/logout")
def logout():
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)