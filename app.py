import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
 
app = Flask(__name__)
app.secret_key = 'jurema'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id, nome, email):
        self.id = id
        self.nome = nome
        self.email = email

def iniciar_conexao():
    conexao = sqlite3.connect('banco.db')
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL) 
    """) 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lembretes ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            detalhes TEXT NOT NULL)
    """)
    conexao.commit()
    conexao.close()

iniciar_conexao()

def obter_conexao():
    conexao = sqlite3.connect('banco.db')
    conexao.row_factory = sqlite3.Row
    return conexao

@login_manager.user_loader
def load_user(user_id):
    conexao = obter_conexao()
    usuario = conexao.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,)).fetchone()
    conexao.close()
    if usuario:
        return User(usuario["id"], usuario["nome"], usuario["email"])
    return None

@app.route("/", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")

        senha_hash = generate_password_hash(senha)

        conexao = obter_conexao()
        conexao.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha_hash))
        conexao.commit()
        conexao.close()
        return redirect(url_for("login", mensagem="cadastro_sucesso"))

    return render_template("cadastro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("inicio"))
    mensagem = request.args.get("mensagem")

    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        conexao = obter_conexao()
        usuario = conexao.execute("SELECT * FROM usuarios WHERE email = ?",(email,)).fetchone()
        conexao.close()

        if usuario and check_password_hash(usuario["senha"], senha):
            user = User(usuario["id"], usuario["nome"], usuario["email"])
            login_user(user)
            return redirect(url_for("inicio"))
    
        return render_template("login.html", mensagem="login_invalido")

    return render_template("login.html", mensagem=mensagem)

@app.route("/inicio")
@login_required
def inicio():
    return render_template("inicio.html", nome=current_user.nome)
    

@app.route("/ver")
@login_required
def ver():
    conexao = obter_conexao()
    conexao.row_factory = sqlite3.Row
    lembretes_db = conexao.execute("SELECT * FROM lembretes").fetchall()
    conexao.close()
    return render_template("ver_lembretes.html", lembretes=lembretes_db)


@app.route("/criar", methods=["GET", "POST"])
@login_required
def criar():
    if request.method == "POST":
        titulo = request.form.get("titulo")
        detalhes = request.form.get("detalhes")

        conexao = obter_conexao()
        conexao.execute("INSERT INTO lembretes (titulo, detalhes) VALUES (?, ?)", (titulo, detalhes))
        conexao.commit()
        conexao.close()

        return redirect(url_for("ver"))

    return render_template("criar_lembrete.html")


@app.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
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
@login_required
def excluir(id):
    conexao = obter_conexao()
    conexao.execute("DELETE FROM lembretes WHERE id = ?", (id,))
    conexao.commit()
    conexao.close()
    return redirect(url_for("ver"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)