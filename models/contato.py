from peewee import Model, AutoField, CharField, SQL
from playhouse.postgres_ext import BinaryJSONField, DateTimeTZField
from database.conexao import db

class Contato(Model):
    cd_contato = AutoField()
    nm_contato = CharField(max_length=80)
    email = CharField(max_length=120, unique=True)
    celular = CharField(max_length=20, unique=True)
    comentario = CharField(max_length=200)
    indicadores = BinaryJSONField(default=list)
    dt_cadastro = DateTimeTZField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        database = db
        table_name = "tb_contato"        

    @classmethod
    def inserir(cls, dados):
        return cls.create(
            nm_contato=dados.get("nm_contato"),
            email=dados.get("email"),
            celular=dados.get("celular"),
            comentario=dados.get("comentario"),
            indicadores=dados.get("indicadores") or []
        )

    @classmethod
    def buscar_nmcontato(cls, nm_contato):
        return cls.select().where(cls.nm_contato == nm_contato)

    @classmethod
    def buscar_email(cls, email):
        return cls.select().where(cls.email == email)

    @classmethod
    def buscar_celular(cls, celular):
        return cls.select().where(cls.celular == celular)

    @classmethod
    def atualizar(cls, cd_contato, dados):
        return (cls.update(
            nm_contato=dados.get("nm_contato"),
            email=dados.get("email"),
            celular=dados.get("celular"),
            comentario=dados.get("comentario"),
            indicadores=dados.get("indicadores") or []
        ).where(cls.cd_contato == cd_contato).execute())

    @classmethod
    def excluir(cls, cd_contato):
        return cls.delete().where(cls.cd_contato == cd_contato).execute()