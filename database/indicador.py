from peewee import Model, BigAutoField, IntegerField, CharField, ForeignKeyField, DecimalField, BooleanField, DateField, DateTimeField
from database.conexao import db


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