from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

from models import db, Usuario, Transacao
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
database_url = os.getenv("DATABASE_URL", "sqlite:///database.db")
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
db.init_app(app)
csrf = CSRFProtect(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        if Usuario.query.filter_by(email=email).first():
            return render_template("registrar.html", erro="Esse email já está cadastrado.")
        
        if len(senha) < 8:
            return render_template("registrar.html", erro="A senha deve ter pelo menos 6 caracteres.")
        
        if not any(c.isupper() for c in senha):
            return render_template("registrar.html", erro="A senha deve conter pelo menos uma letra maiúscula.")
        
        if not any(c.isdigit() for c in senha):
            return render_template("registrar.html", erro="A senha precisa ter pelo menos um número.")
        
        novo_usuario = Usuario(email=email)
        novo_usuario.set_senha(senha)
        db.session.add(novo_usuario)
        db.session.commit()

        login_user(novo_usuario)
        return redirect("/")

    return render_template("registrar.html")


@app.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.checar_senha(senha):
            login_user(usuario)
            return redirect("/")

        return render_template("login.html", erro="Email ou senha incorretos.")

    return render_template("login.html")

@app.errorhandler(429)
def limite_tentativas(e):
    return render_template("login.html", erro="Muitas tentativas de login. Aguarde um minuto e tente novamente."), 429

@app.route("/login-visitante")
def logar_visitante():
    email_demo = os.getenv("DEMO_EMAIL")
    usuario = Usuario.query.filter_by(email=email_demo).first()

    if usuario:
        login_user(usuario)
        return redirect("/")

    return redirect("/login")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route("/")
@login_required
def home():
    entradas = db.session.query(db.func.sum(Transacao.valor)).filter_by(tipo="entrada", usuario_id=current_user.id).scalar() or 0
    saidas = db.session.query(db.func.sum(Transacao.valor)).filter_by(tipo="saida", usuario_id=current_user.id).scalar() or 0
    lucro = entradas - saidas

    categorias = db.session.query(
        Transacao.categoria, db.func.sum(Transacao.valor)
    ).filter_by(tipo="saida", usuario_id=current_user.id).group_by(Transacao.categoria).all()

    
    nomes_categorias = [c[0] for c in categorias]
    valores_categorias = [c[1] for c in categorias]

    
    return render_template(
    "index.html",
    entradas=entradas, saidas=saidas, lucro=lucro,
    nomes_categorias=nomes_categorias, valores_categorias=valores_categorias,
)

@app.route("/nova", methods=["GET", "POST"])
@login_required
def nova_transacao():
    if request.method == "POST":
        nova = Transacao(
            tipo=request.form["tipo"],
            valor=float(request.form["valor"]),
            categoria=request.form["categoria"],
            descricao=request.form["descricao"],
            usuario_id=current_user.id
        )
        db.session.add(nova)
        db.session.commit()
        return redirect("/nova")

    return render_template("nova_transacao.html")


@app.route("/historico")
@login_required
def historico():
    transacoes = Transacao.query.filter_by(usuario_id=current_user.id).all()
    return render_template("historico.html", transacoes=transacoes)


@app.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_transacao(id):
    t = Transacao.query.get_or_404(id)
    if t.usuario_id != current_user.id:
        return "Acesso negado", 403

    if request.method == "POST":
        t.tipo = request.form["tipo"]
        t.valor = float(request.form["valor"])
        t.categoria = request.form["categoria"]
        t.descricao = request.form["descricao"]
        db.session.commit()
        return redirect("/historico")

    return render_template("editar_transacao.html", t=t)


@app.route("/excluir/<int:id>", methods=["POST"])
@login_required
def excluir_transacao(id):
    t = Transacao.query.get_or_404(id)
    if t.usuario_id != current_user.id:
        return "Acesso negado", 403

    db.session.delete(t)
    db.session.commit()
    return redirect("/historico")

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "False") == "True"
    app.run(debug=debug_mode)