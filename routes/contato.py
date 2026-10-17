from flask import Blueprint, render_template, request
from peewee import IntegrityError
from models.contato import Contato
from database.conexao import conectar

contato_bp = Blueprint("contato", __name__)

@contato_bp.route("/contato", methods=["GET", "POST"])
def contato():
    mensagem = None

    if request.method == "POST":
        nm_contato = request.form.get("nm_contato", "").strip()
        email = request.form.get("email", "").strip().lower()
        celular = request.form.get("celular", "").strip()
        comentario = request.form.get("comentario", "").strip()
        dt_nascimento = request.form.get("dt_nascimento") or None
        celular = "".join(filter(str.isdigit, celular)) or None

        try:
            with conectar():
                Contato.inserir(nm_contato=nm_contato.strip(), email=email, celular=celular, comentario=comentario, dt_nascimento=dt_nascimento)
            mensagem = "Contato cadastrado com sucesso."

        except IntegrityError:
            mensagem = "E-mail ou celular já cadastrado."

    return render_template("contato.html", mensagem=mensagem)
