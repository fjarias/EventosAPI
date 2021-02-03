##
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from sqlalchemy import desc

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///abc.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

##
# Recurso Evento *********************************************************************************************
class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    categoria = db.Column(db.String(50))
    lugar = db.Column(db.String(255))
    direccion = db.Column(db.String(255))
    fecha_creacion = db.Column(db.String(50))
    fecha_inicio = db.Column(db.String(50))
    fecha_fin = db.Column(db.String(50))
    evento_virtual = db.Column(db.Boolean)
    usuario = db.Column(db.String(50))


class Evento_Schema(ma.Schema):
    class Meta:
        fields = ("id", "nombre", "categoria", "lugar", "direccion", "fecha_creacion",
                  "fecha_inicio", "fecha_fin", "evento_virtual", "usuario")

post_schema_ev = Evento_Schema()
posts_schema_ev = Evento_Schema(many=True)


class RecursoListarEventosUsuario(Resource):
    def get(self, usuario):
        eventos = Evento.query.filter_by(usuario=usuario).order_by(desc(Evento.fecha_creacion))
        return posts_schema_ev.dump(eventos)


class RecursoListarEventos(Resource):
    def get(self):
        eventos = Evento.query.all()
        return posts_schema_ev.dump(eventos)
    def post(self):
        nuevo_evento = Evento(
            nombre=request.json['nombre'],
            categoria=request.json['categoria'],
            lugar=request.json['lugar'],
            direccion=request.json['direccion'],
            fecha_creacion=request.json['fecha_creacion'],
            fecha_inicio=request.json['fecha_inicio'],
            fecha_fin=request.json['fecha_fin'],
            evento_virtual=request.json['evento_virtual'],
            usuario=request.json['usuario']
        )
        db.session.add(nuevo_evento)
        db.session.commit()
        return post_schema_ev.dump(nuevo_evento)


class RecursoUnEvento(Resource):
    def get(self, id_evento):
        evento = Evento.query.get_or_404(id_evento)
        return post_schema_ev.dump(evento)

    def put(self, id_evento):
        evento = Evento.query.get_or_404(id_evento)
        if 'nombre' in request.json:
            evento.nombre = request.json['nombre']
        if 'categoria' in request.json:
            evento.categoria = request.json['categoria']
        if 'lugar' in request.json:
            evento.lugar = request.json['lugar']
        if 'direccion' in request.json:
            evento.direccion = request.json['direccion']
        if 'fecha_inicio' in request.json:
            evento.fecha_creacion = request.json['fecha_creacion']
        if 'fecha_inicio' in request.json:
            evento.fecha_inicio = request.json['fecha_inicio']
        if 'fecha_fin' in request.json:
            evento.fecha_fin= request.json['fecha_fin']
        if 'evento_virtual' in request.json:
            evento.evento_virtual = request.json['evento_virtual']
        db.session.commit()
        return post_schema_ev.dump(evento)

    def delete(self, id_evento):
        evento = Evento.query.get_or_404(id_evento)
        db.session.delete(evento)
        db.session.commit()
        return '', 204

api.add_resource(RecursoListarEventos, '/eventos')
api.add_resource(RecursoListarEventosUsuario, '/eventos/<string:usuario>')
api.add_resource(RecursoUnEvento, '/eventos/<int:id_evento>')
if __name__ == '__main__':
    app.run(debug=True)
