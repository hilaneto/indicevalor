from flask import Blueprint, render_template, request
from peewee import IntegrityError
from models.contato import Contato
from database.conexao import conectar

contato_bp = Blueprint("contato", __name__)

INDICADORES = {"DOLAR_COMERCIAL": "Dólar Comercial",
               "DOLAR_TURISMO": "Dólar Turismo",
               "EURO": "Euro",
               "BITCOIN": "Bitcoin",
               "IPCA": "IPCA",
               "INPC": "INPC",
               "IGPM": "IGP-M",
               "IBOVESPA": "Ibovespa",
               "SELIC": "Selic",
               "CDI": "CDI",
               "TR": "TR",
               "SALARIO": "Salário Mínimo"
             }

@contato_bp.route("/contato", methods=["GET", "POST"])
def contato():
    mensagem = None
    sucesso = False

    if request.method == "POST":
        dados = {"nm_contato": request.form.get("nm_contato", "").strip(),
                 "email": request.form.get("email", "").strip().lower(),
                 "celular": "".join(filter(str.isdigit, request.form.get("celular", ""))),
                 "comentario": request.form.get("comentario", "").strip(),
                 "indicadores": request.form.getlist("indicadores")
                }

        if not all(dados[campo] for campo in ("nm_contato", "email", "celular", "comentario")):
            mensagem = "Preencha todos os campos obrigatórios."

        elif any(ind not in INDICADORES for ind in dados["indicadores"]):
            mensagem = "Um ou mais indicadores selecionados são inválidos."

        elif len(dados["nm_contato"]) > 80 or len(dados["email"]) > 120 or len(dados["celular"]) > 20 or len(dados["comentario"]) > 200:
            mensagem = "Um ou mais campos ultrapassam o tamanho permitido."

        else:
            try:
                with conectar():
                    Contato.inserir(dados)

                mensagem = "Contato cadastrado com sucesso."
                sucesso = True

            except IntegrityError:
                mensagem = "Não foi possível cadastrar. Verifique se o e-mail ou celular já está cadastrado."


    return render_template("contato.html", mensagem=mensagem, sucesso=sucesso, indicadores=INDICADORES)