from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'jurema'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    senha = db.Column(db.String(256), nullable=False)
    lembretes = db.relationship('Lembrete', backref='autor', lazy=True)

class Lembrete(db.Model):
    __tablename__ = 'lembretes'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    detalhes = db.Column(db.Text, nullable=False)

    categoria = db.Column(db.String(50), nullable=False)
    prioridade = db.Column(db.String(20), nullable=False)
    data = db.Column(db.String(20), nullable=False)
    concluido = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")

        senha_hash = generate_password_hash(senha)
        
        novo_usuario = User(nome=nome, email=email, senha=senha_hash)
        db.session.add(novo_usuario)
        db.session.commit()
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

        usuario = User.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
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
    lembretes_db = Lembrete.query.filter_by(user_id=current_user.id).all()
    return render_template("ver_lembretes.html", lembretes=lembretes_db)


@app.route("/criar", methods=["GET", "POST"])
@login_required
def criar():
    if request.method == "POST":
        titulo = request.form.get("titulo")
        detalhes = request.form.get("detalhes")
        categoria = request.form.get("categoria")
        prioridade = request.form.get("prioridade")
        data = request.form.get("data")

        novo_lembrete = Lembrete(
            titulo=titulo,
            detalhes=detalhes,
            categoria=categoria,
            prioridade=prioridade,
            data=data,
            concluido=False,
            user_id=current_user.id
        )

        db.session.add(novo_lembrete)
        db.session.commit()

        return redirect(url_for("ver"))

    return render_template("criar_lembrete.html")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    lembrete = Lembrete.query.get_or_404(id)

    if request.method == "POST":
        lembrete.titulo = request.form.get("titulo")
        lembrete.detalhes = request.form.get("detalhes")
        lembrete.categoria = request.form.get("categoria")
        lembrete.prioridade = request.form.get("prioridade")
        lembrete.data = request.form.get("data")
        db.session.commit()
        return redirect(url_for("ver"))

    return render_template("editar_lembrete.html", lembrete=lembrete)


@app.route("/excluir/<int:id>")
@login_required
def excluir(id):
    lembrete = Lembrete.query.get_or_404(id)
    db.session.delete(lembrete)
    db.session.commit()
    return redirect(url_for("ver"))

@app.route("/concluir/<int:id>")
@login_required
def concluir(id):
    lembrete = Lembrete.query.get_or_404(id)

    if lembrete.concluido:
        lembrete.concluido = False
    else:
        lembrete.concluido = True

    db.session.commit()

    return redirect(url_for("ver"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)