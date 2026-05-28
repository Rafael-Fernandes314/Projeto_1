import sqlite3
from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)

def iniciar_banco():
    conexao = sqlite3.connect('banco.db')
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            senha VARCHAR(20) NOT NULL UNIQUE) 
    """) 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lembretes ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            detalhes TEXT NOT NULL)
    """)
    conexao.commit()
    conexao.close()

iniciar_banco()

def obter_conexao():
    conexao = sqlite3.connect('banco.db')
    conexao.row_factory = sqlite3.Row
    return conexao


def obter_usuario(usuario_id):
    if not usuario_id:
        return None
    conexao = obter_conexao()
    usuario = conexao.execute("SELECT nome FROM usuarios WHERE id = ?", (usuario_id,)).fetchone()
    conexao.close()
    return usuario['nome'] if usuario else None


@app.route("/", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")

        conexao = obter_conexao()
        conexao.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
        conexao.commit()
        conexao.close()

        return redirect(url_for("login", mensagem="cadastro_sucesso"))

    return render_template("cadastro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    mensagem = request.args.get('mensagem')

    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha") 
        
        conexao = obter_conexao()
        usuario = conexao.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha)).fetchone()
        conexao.close()

        if usuario:
            resp = make_response(redirect(url_for("inicio")))
            resp.set_cookie("user_id", str(usuario['id']), httponly=True)
            return resp
        return render_template("login.html", mensagem="login_invalido")

    return render_template("login.html", mensagem=mensagem)


@app.route("/inicio")
def inicio():
    user_id = request.cookies.get('user_id')
    nome = obter_usuario(user_id)
    if nome is None:
        return redirect(url_for("login", mensagem="precisa_logar"))
    return render_template("inicio.html", nome=nome)


@app.route("/ver")
def ver():
    conexao = obter_conexao()
    conexao.row_factory = sqlite3.Row
    lembretes_db = conexao.execute("SELECT * FROM lembretes").fetchall()
    conexao.close()
    return render_template("ver_lembretes.html", lembretes=lembretes_db)


@app.route("/criar", methods=["GET", "POST"])
def criar():
    if request.method == "POST":
        titulo = request.form.get("titulo")
        detalhes = request.form.get("detalhes")

        conexao = obter_conexao()
        conexao.execute("""INSERT INTO lembretes (titulo, detalhes) VALUES (?, ?)""", (titulo, detalhes))
        conexao.commit()
        conexao.close()

        return redirect(url_for("ver"))

    return render_template("criar_lembrete.html")


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conexao = obter_conexao()

    if request.method == "POST":
        titulo = request.form.get("titulo")
        detalhes = request.form.get("detalhes")

        conexao.execute("UPDATE lembretes SET titulo = ?, detalhes = ? WHERE id = ?", (titulo, detalhes, id))
        conexao.commit()
        conexao.close()
        return redirect(url_for("ver"))

    lembrete = conexao.execute("SELECT * FROM lembretes WHERE id = ?", (id,)).fetchone()
    conexao.close()
    return render_template("editar_lembrete.html", lembrete=lembrete)


@app.route("/excluir/<int:id>")
def excluir(id):
    conexao = obter_conexao()
    conexao.execute("DELETE FROM lembretes WHERE id = ?", (id,))
    conexao.commit()
    conexao.close()
    return redirect(url_for("ver"))


@app.route("/logout")
def logout():
    resp = make_response(redirect(url_for("login")))
    resp.delete_cookie("user_id")
    return resp


if __name__ == "__main__":
    app.run(debug=True)