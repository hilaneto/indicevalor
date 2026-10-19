from peewee import Model, AutoField, DecimalField, DateTimeField, DateField, BooleanField
from datetime import datetime
from database.conexao import db
from database.conexao import conectar
from database.crud_base import CrudBase

class Tr(Model):
    cd_tr = AutoField()
    indice = DecimalField(max_digits=8, decimal_places=5)
    status = BooleanField(default=False, null=False)
    dt_referencia = DateField(null=False)
    dt_atualizacao = DateTimeField(default=datetime.now, null=False)
    
    class Meta:
        database = db
        table_name = "tb_tr"

    @staticmethod
    def atual():
        with conectar():
            return (Tr.select().where(Tr.status == True).order_by(Tr.dt_referencia.desc()).first())

    @staticmethod
    def ultimos_6m():
        with conectar():
            return list(Tr.select().where(Tr.status == True).order_by(Tr.dt_referencia.desc()).limit(6))

class CrudTr(CrudBase):
    def __init__(self):
        super().__init__(Tr)
