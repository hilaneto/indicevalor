from peewee import Model, BigAutoField, IntegerField, CharField, ForeignKeyField, DecimalField, BooleanField, DateField, DateTimeField
from database.conexao import db, conectar
from peewee import fn

class IndicadorInfo(Model):
    cd_indicador = IntegerField(primary_key=True)
    nm_indicador = CharField(max_length=50, unique=True)

    class Meta:
        database = db
        table_name = "tb_indicador_info"


class Indicador(Model):
    cd_registro = BigAutoField()
    cd_indicador = ForeignKeyField(IndicadorInfo, column_name="cd_indicador", backref="historicos")
    valor = DecimalField(max_digits=18, decimal_places=5)
    status = BooleanField(default=True)
    dt_referencia = DateField()
    dt_atualizacao = DateTimeField()

    class Meta:
        database = db
        table_name = "tb_indicador"

    @staticmethod
    def consultar(nome, limite=1):
        with conectar():
            consulta = (Indicador.select()
                        .join(IndicadorInfo)
                        .where((IndicadorInfo.nm_indicador == nome.upper()) &
                               (Indicador.status == True))
                        .order_by(Indicador.dt_referencia.desc())
                        .limit(limite))

            registros = list(consulta)
            return registros[0] if limite == 1 and registros else (None if limite == 1 else registros)

    @staticmethod
    def atual(nome):
        return Indicador.consultar(nome)

    @staticmethod
    def atuais():
        with conectar():
            ultimas_datas = (Indicador
                .select(
                    Indicador.cd_indicador,
                    fn.MAX(Indicador.dt_referencia).alias("ultima_data"))
                .where(Indicador.status == True)
                .group_by(Indicador.cd_indicador)
                .alias("ultimas"))

            consulta = (Indicador
                .select(Indicador, IndicadorInfo)
                .join(IndicadorInfo)
                .switch(Indicador)
                .join(ultimas_datas, on=(
                    (Indicador.cd_indicador == ultimas_datas.c.cd_indicador) &
                    (Indicador.dt_referencia == ultimas_datas.c.ultima_data)))
                .where(Indicador.status == True))

            return {registro.cd_indicador.nm_indicador: registro for registro in consulta}

    @staticmethod
    def ultimos(nome, quantidade=6):
        return Indicador.consultar(nome, quantidade)