from flask import Blueprint, render_template, send_from_directory, session, redirect, url_for, Response
from datetime import datetime
import calendar
from models.indicador import Indicador
from models.moeda import Moeda
from models.temperatura import Temperatura
from models.ibovespa import Ibovespa
from models.pib_valores import PibValores
from models.indicador_info import IndicadorInfo


home_bp = Blueprint('home', __name__)

def formatar_real(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_real_4casas(valor):
    return f"R$ {valor:,.4f}".replace(",", "X").replace(".", ",").replace("X", ".")

@home_bp.route("/")
def home():
    indicadores = Indicador.atuais()

    meses = ["Janeiro", "Fevereiro", "Março", "Abril",
             "Maio", "Junho", "Julho", "Agosto",
             "Setembro", "Outubro", "Novembro", "Dezembro"]

    def percentual(nome, casas=2, sinal=False):
        registro = indicadores.get(nome)
        if not registro:
            return "Sem dados", ""

        valor = f"{float(registro.valor):+.{casas}f}%" if sinal else f"{float(registro.valor):.{casas}f}%"
        dt = registro.dt_referencia
        return valor.replace(".", ","), f"{meses[dt.month - 1]} - {dt.year}"

    vl_ipca_formato, dtref_ipca = percentual("IPCA")
    vl_inpc, dtref_inpc = percentual("INPC")
    vl_cdi, dtref_cdi = percentual("CDI")
    vl_tr, dtref_tr = percentual("TR", 4)
    vl_igpm, dtref_igpm = percentual("IGPM")

    vl_pib_variacao, dtref_pib_variacao = percentual("PIB", sinal=True)
    if indicadores.get("PIB"):
        dt = indicadores["PIB"].dt_referencia
        dtref_pib_variacao = f"{(dt.month - 1) // 3 + 1}º trimestre de {dt.year}"

    selic = indicadores.get("SELIC")
    vl_selic_formato = f"{float(selic.valor):.2f}%".replace(".", ",") if selic else "Sem dados"
    dtref_selic = selic.dt_referencia.strftime("%d/%m/%Y") if selic else ""

    salario = indicadores.get("SALARIO")
    vl_salario = formatar_real(float(salario.valor)) if salario else "Sem dados"
    dtref_salario = salario.dt_referencia.strftime("%d/%m/%Y") if salario else ""

    populacao = indicadores.get("POPULACAO")
    vl_populacao = f"{int(populacao.valor):,}".replace(",", ".") if populacao else "Sem dados"
    dtref_populacao = str(populacao.dt_referencia.year) if populacao else ""


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

    # PIB — Valor monetário ---------------------------------------
    pib_valores = PibValores.atual()

    if pib_valores:
        vl_pib_monetario = f"R$ {pib_valores.valor_milhoes / 1_000_000:,.3f}".replace(",", "X").replace(".", ",").replace("X", ".") + " trilhões"
        dt = pib_valores.dt_referencia
        dtref_pib_monetario = f"{(dt.month - 1) // 3 + 1}º trimestre de {dt.year}"
    else:
        vl_pib_monetario = "Sem dados"
        dtref_pib_monetario = ""        

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
        vl_pib_variacao=vl_pib_variacao,
        dtref_pib_variacao=dtref_pib_variacao,
        vl_populacao=vl_populacao,
        dtref_populacao=dtref_populacao,
        vl_pib_monetario=vl_pib_monetario,
        dtref_pib_monetario=dtref_pib_monetario,
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