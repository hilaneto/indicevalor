from peewee import Model, AutoField, CharField, TextField, BooleanField, DateTimeField
from database.conexao import db, conectar


class IndicadorInfo(Model):
    cd_indicador = AutoField()
    nm_indicador = CharField(max_length=50, unique=True)
    titulo = CharField(max_length=150)
    descricao = TextField()
    periodicidade = CharField(max_length=30, null=True)
    fonte = CharField(max_length=150, null=True)
    url_fonte = TextField(null=True)
    fl_ativo = BooleanField(default=True)
    dt_atualizacao = DateTimeField()

    class Meta:
        database = db
        table_name = "tb_indicador_info"

    @staticmethod
    def buscar():
        with conectar():
            return {
                item.nm_indicador: {
                    "titulo": item.titulo,
                    "descricao": item.descricao,
                    "periodicidade": item.periodicidade,
                    "fonte": item.fonte,
                    "url_fonte": item.url_fonte
                }
                for item in IndicadorInfo.select().where(IndicadorInfo.fl_ativo == True)
            }