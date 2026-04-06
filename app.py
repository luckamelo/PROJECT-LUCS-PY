from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import db, User, Instituicao, Log

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        senha = request.form.get("senha")

        user = User.query.filter_by(email=email).first()

        if user is not None and check_password_hash(user.senha, senha):

            login_user(user)

            log = Log(usuario=user.nome, acao="Login no sistema")
            db.session.add(log)
            db.session.commit()

            return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = generate_password_hash(request.form.get("senha"))

        novo = User(nome=nome,email=email,senha=senha,tipo="admin")

        db.session.add(novo)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/instituicoes", methods=["GET","POST"])
@login_required
def instituicoes():

    if request.method == "POST":

        nome = request.form.get("nome")
        endereco = request.form.get("endereco")
        responsavel = request.form.get("responsavel")

        inst = Instituicao(
            nome=nome,
            endereco=endereco,
            responsavel=responsavel
        )

        db.session.add(inst)
        db.session.commit()

        log = Log(usuario="admin",acao="Instituição cadastrada")
        db.session.add(log)
        db.session.commit()

    lista = Instituicao.query.all()

    return render_template("instituicoes.html",lista=lista)


@app.route("/testes")
@login_required
def testes():

    log = Log(usuario="sistema",acao="Ambiente de testes executado")
    db.session.add(log)
    db.session.commit()

    return render_template("testes.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)
