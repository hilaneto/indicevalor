from flask import Blueprint, render_template, send_from_directory, session, redirect, url_for, Response
from datetime import datetime
import calendar
from models.moeda import Moeda
from models.ipca import Ipca
from models.inpc import Inpc
from models.tr import Tr
from models.cdi import Cdi
from models.selic import Selic
from models.salario import Salario
from models.temperatura import Temperatura
from models.ibovespa import Ibovespa
from models.igpm import Igpm
from models.indicador_info import IndicadorInfo


home_bp = Blueprint('home', __name__)

def formatar_real(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_real_4casas(valor):
    return f"R$ {valor:,.4f}".replace(",", "X").replace(".", ",").replace("X", ".")

@home_bp.route("/")
def home():

    # Moedas ----------------------------------------------------
    dolarc_compra = Moeda.atual("USDCC")
    dolarc_venda = Moeda.atual("USDCV")
    dolart_compra = Moeda.atual("USDTC")
    dolart_venda = Moeda.atual("USDTV")
    euro_atual = Moeda.atual("EUR")
    bitcoin_atual = Moeda.atual("BTC")

    vl_dolarc_compra = formatar_real_4casas(float(dolarc_compra.valor))
    vl_dolarc_venda = formatar_real_4casas(float(dolarc_venda.valor))
    vl_dolart_compra = formatar_real_4casas(float(dolart_compra.valor))
    vl_dolart_venda = formatar_real_4casas(float(dolart_venda.valor))
    vl_euro = formatar_real_4casas(float(euro_atual.valor))
    vl_bitcoin = formatar_real(float(bitcoin_atual.valor))

    dtref_dolarc_compra = dolarc_compra.dt_referencia.strftime("%d/%m/%Y %H:%M")
    dtref_dolarc_venda = dolarc_venda.dt_referencia.strftime("%d/%m/%Y %H:%M")
    dtref_dolart_compra = dolart_compra.dt_referencia.strftime("%d/%m/%Y %H:%M")
    dtref_dolart_venda = dolart_venda.dt_referencia.strftime("%d/%m/%Y %H:%M")

    dtref_euro = euro_atual.dt_referencia.strftime("%d/%m/%Y %H:%M")
    dtref_bitcoin = bitcoin_atual.dt_referencia.strftime("%d/%m/%Y %H:%M")

    # IPCA ------------------------------------------------------
    meses = ["Janeiro", "Fevereiro", "Março", "Abril",
             "Maio", "Junho", "Julho", "Agosto",
             "Setembro", "Outubro", "Novembro", "Dezembro"]

    ipca_atual = Ipca.atual()
    vl_ipca = float(ipca_atual.indice)
    vl_ipca_formato = f"{vl_ipca:.2f}%".replace(".", ",")
    dt = ipca_atual.dt_referencia
    dtref_ipca = f"{meses[dt.month - 1]} - {dt.year}"
 

    # INPC -----------------------------------------------------
    inpc_atual = Inpc.atual()

    if inpc_atual:
        vl_inpc = f"{float(inpc_atual.indice):.2f}%".replace(".", ",")
        dt = inpc_atual.dt_referencia
        dtref_inpc = f"{meses[dt.month - 1]} - {dt.year}"
    else:
        vl_inpc = "Sem dados"
        dtref_inpc = ""

    # CDI -----------------------------------------------------
    cdi_atual = Cdi.atual()

    if cdi_atual:
        vl_cdi = f"{float(cdi_atual.indice):.2f}%".replace(".", ",")
        dt = cdi_atual.dt_referencia
        dtref_cdi = f"{meses[dt.month - 1]} - {dt.year}"
    else:
        vl_cdi = "Sem dados"
        dtref_cdi = ""

    # TR -----------------------------------------------------
    tr_atual = Tr.atual()

    if tr_atual:
        vl_tr = f"{float(tr_atual.indice):.4f}%".replace(".", ",")
        dt = tr_atual.dt_referencia
        dtref_tr = f"{meses[dt.month - 1]} - {dt.year}"
    else:
        vl_tr = "Sem dados"
        dtref_tr = ""


    # IGP-M -----------------------------------------------------
    igpm_atual = Igpm.atual()

    if igpm_atual:
        vl_igpm = f"{float(igpm_atual.indice):.2f}%".replace(".", ",")
        dt = igpm_atual.dt_referencia
        dtref_igpm = f"{meses[dt.month - 1]} - {dt.year}"
    else:
        vl_igpm = "Sem dados"
        dtref_igpm = ""


    # Selic -----------------------------------------------------
    selic_atual = Selic.atual()
    vl_selic = float(selic_atual.indice)
    vl_selic_formato = f"{vl_selic:.2f}%".replace(".", ",")
    dtref_selic = selic_atual.dt_referencia.strftime("%d/%m/%Y")

    # Salário Mínimo --------------------------------------------
    salario_atual = Salario.atual()
    vl_salario = formatar_real(float(salario_atual.vl_salario))
    dtref_salario = salario_atual.dt_referencia.strftime("%d/%m/%Y")

    # Temperaturas ----------------------------------------------
    temperaturas = []

    for registro in Temperatura.atuais():
        temperaturas.append({
            "regiao": registro.regiao,
            "cidade": registro.cidade,
            "temperatura": registro.temperatura_exibicao,
            "dt_referencia": registro.dt_referencia,
        })

    # Calendário -------------------------------------------------
    dt_atual = datetime.now()

    ano_atual = dt_atual.year
    numero_mes_atual = dt_atual.month

    if numero_mes_atual == 1:
        ano_anterior, numero_mes_anterior = ano_atual - 1, 12
    else:
        ano_anterior, numero_mes_anterior = ano_atual, numero_mes_atual - 1

    if numero_mes_atual == 12:
        ano_proximo, numero_mes_proximo = ano_atual + 1, 1
    else:
        ano_proximo, numero_mes_proximo = ano_atual, numero_mes_atual + 1

    cal = calendar.Calendar(firstweekday=6)

    mes_anterior = f"{meses[numero_mes_anterior - 1]} {ano_anterior}"
    mes_atual = f"{meses[numero_mes_atual - 1]} {ano_atual}"
    mes_proximo = f"{meses[numero_mes_proximo - 1]} {ano_proximo}"

    calendario_anterior = cal.monthdayscalendar(ano_anterior, numero_mes_anterior)
    calendario_atual = cal.monthdayscalendar(ano_atual, numero_mes_atual)
    calendario_proximo = cal.monthdayscalendar(ano_proximo, numero_mes_proximo)


    # Ibovespa ----------------------------------------------
    ibovespa_atual = Ibovespa.atual()
    vl_ibovespa = f"{float(ibovespa_atual.pontos):,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    vl_ibovespa_variacao = f"{float(ibovespa_atual.variacao):,.2f}%".replace(",", "X").replace(".", ",").replace("X", ".")
    dtref_ibovespa = ibovespa_atual.dt_referencia.strftime("%d/%m/%Y %H:%M")

    # indicadores_info -------
    indicadores_info = IndicadorInfo.buscar()


    return render_template(
        "home.html",
        vl_dolarc_compra =vl_dolarc_compra,
        dtref_dolarc_compra=dtref_dolarc_compra,
        vl_dolarc_venda =vl_dolarc_venda,
        dtref_dolarc_venda=dtref_dolarc_venda,
        vl_dolart_venda=vl_dolart_venda,
        dtref_dolart_venda=dtref_dolart_venda,
        vl_dolart_compra=vl_dolart_compra,
        dtref_dolart_compra=dtref_dolart_compra,
        vl_euro=vl_euro,
        dtref_euro=dtref_euro,
        vl_bitcoin=vl_bitcoin,
        dtref_bitcoin=dtref_bitcoin,
        vl_ipca=vl_ipca_formato,
        dtref_ipca=dtref_ipca,
        vl_selic=vl_selic_formato,
        dtref_selic=dtref_selic,
        vl_salario=vl_salario,
        dtref_salario=dtref_salario,
        temperaturas=temperaturas,
        vl_ibovespa=vl_ibovespa,
        vl_ibovespa_variacao=vl_ibovespa_variacao,
        dtref_ibovespa=dtref_ibovespa,
        dt_atual=dt_atual,
        mes_anterior=mes_anterior,
        mes_atual=mes_atual,
        mes_proximo=mes_proximo,
        calendario_anterior=calendario_anterior,
        calendario_atual=calendario_atual,
        calendario_proximo=calendario_proximo,
        vl_igpm=vl_igpm,
        dtref_igpm=dtref_igpm,
        vl_inpc=vl_inpc,
        dtref_inpc=dtref_inpc,
        vl_cdi=vl_cdi,
        dtref_cdi=dtref_cdi,
        vl_tr=vl_tr,
        dtref_tr=dtref_tr,
        indicadores_info=indicadores_info,
    )

@home_bp.route("/sistema")
def sistema():
    if "usuario_id" not in session:
        return redirect(url_for("home.home"))

    return render_template("sistema.html")


# SEO - Google -----------------------------------------------

@home_bp.route("/robots.txt")
def robots():
    conteudo = """User-agent: *
Allow: /
Disallow: /logar
Disallow: /login
Disallow: /logout
Disallow: /sistema
Disallow: /upload
Disallow: /cdusuario/
Disallow: /cpf/
Disallow: /cnpj/

Sitemap: https://indicevalor.com/sitemap.xml
"""
    return Response(conteudo, mimetype="text/plain")


@home_bp.route("/sitemap.xml")
def sitemap():
    urls = ["/", "/contato", "/downloads"]

    conteudo = '<?xml version="1.0" encoding="UTF-8"?>\n'
    conteudo += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for url in urls:
        conteudo += f"    <url><loc>https://indicevalor.com{url}</loc></url>\n"

    conteudo += "</urlset>"

    return Response(conteudo, mimetype="application/xml")