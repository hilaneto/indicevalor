from database.conexao import conectar
from database.indicador import Indicador, IndicadorInfo
from database.crud_base import CrudBase


class Ipca:

    @staticmethod
    def atual():
        with conectar():
            indicador = IndicadorInfo.get(IndicadorInfo.nm_indicador == "IPCA")

            return (Indicador.select()
                    .where((Indicador.cd_indicador == indicador.cd_indicador) &
                           (Indicador.status == True))
                    .order_by(Indicador.dt_referencia.desc())
                    .first())

    @staticmethod
    def ultimos_6m():
        with conectar():
            indicador = IndicadorInfo.get(IndicadorInfo.nm_indicador == "IPCA")

            return list(Indicador.select()
                        .where((Indicador.cd_indicador == indicador.cd_indicador) &
                               (Indicador.status == True))
                        .order_by(Indicador.dt_referencia.desc())
                        .limit(6))


class CrudIpca(CrudBase):
    def __init__(self):
        super().__init__(Indicador)