from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

usuarios_cadastrados = []
lembretes = []


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    nome = request.form.get("nome")
    email = request.form.get("email")

    usuarios_cadastrados.append({
        'nome': nome,
        'email': email
    })

    if request.method == "GET":
        return render_template("cadastro.html")

    return redirect(url_for("login", mensagem="cadastro_sucesso"))


@app.route("/login", methods=["GET", "POST"])
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
    return render_template("inicial.html", nome=nome, lembretes=lembretes)


@app.route("/criar", methods=["GET", "POST"])
def criar():
    if request.method == "POST":
        titulo = request.form.get("titulo")
        detalhes = request.form.get("detalhes")

        lembretes.append({
            "id": len(lembretes),
            "titulo": titulo,
            "detalhes": detalhes
        })

        return redirect(url_for("inicial"))

    return render_template("criar_lembrete.html")


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    lembrete = lembretes[id]

    if request.method == "POST":
        lembrete["titulo"] = request.form.get("titulo")
        lembrete["detalhes"] = request.form.get("detalhes")

        return redirect(url_for("inicial"))

    return render_template("editar_lembrete.html", lembrete=lembrete)


@app.route("/excluir/<int:id>")
def excluir(id):
    lembretes.pop(id)
    return redirect(url_for("inicial"))


@app.route("/logout")
def logout():
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)