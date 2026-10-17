from peewee import Model, AutoField, DecimalField, DateTimeField, DateField, BooleanField
from database.conexao import db
from database.conexao import conectar
from database.crud_base import CrudBase


class Igpm(Model):
    cd_igpm = AutoField(primary_key=True)
    indice = DecimalField(max_digits=8, decimal_places=5)
    status = BooleanField(default=True, null=False)
    dt_referencia = DateField(null=False)
    dt_atualizacao = DateTimeField(null=False)

    class Meta:
        database = db
        table_name = "tb_igpm"

    @staticmethod
    def atual():
        with conectar():
            return (Igpm.select()
                    .where(Igpm.status == True)
                    .order_by(Igpm.dt_referencia.desc())
                    .first())

class CrudIgpm(CrudBase):
    def __init__(self):
        super().__init__(Igpm)