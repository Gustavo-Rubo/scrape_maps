from app import db
# from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from sqlalchemy import DateTime, Integer, String, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr, relationship
from typing import List

class Macro(db.Model):
    __tablename__ = 'macros'

    id:Mapped[int] = mapped_column(primary_key=True)
    nome:Mapped[str] = mapped_column()
    wkt:Mapped[str] = mapped_column()

    micros:Mapped[List['Micro']] = relationship(back_populates='macros')

    def __init__(self, nome, wkt):
        self.nome = nome
        self.wkt = wkt

    def __repr__(self):
        return f"<Macro {self.nome}>"
    
class Submacro(db.Model):
    __tablename__ = 'submacros'

    id:Mapped[int] = mapped_column(primary_key=True)
    nome:Mapped[int] = mapped_column()
    wkt:Mapped[int] = mapped_column()

    micros:Mapped[List['Micro']] = relationship(back_populates='submacros')

    def __init__(self, nome, wkt):
        self.nome = nome
        self.wkt = wkt

    def __repr__(self):
        return f"<Submacro {self.nome}>"
    
# class PalavrasChave(db.Model):
    # id =
    # nome = 
    
class TimestampMixin:
    data_criado: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    data_modificado: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
class Micro(TimestampMixin, db.Model):
    __tablename__ = 'micros'

    id:Mapped[int] = mapped_column(primary_key=True)
    macro_ids:Mapped[List[int]] = mapped_column(ForeignKey('macros.id'))
    submacro_ids:Mapped[List[int]] = mapped_column(ForeignKey('submacros.id'))
    nome:Mapped[str] = mapped_column(db.String())
    panoid:Mapped[str] = mapped_column(db.String())
    origem:Mapped[str] = mapped_column(db.String())
    # lat
    # long
    # palavras_chave
    # object_recognition = db.Column(db.String())
    ocr:Mapped[str] = db.Column(Text())
    descricao:Mapped[str] = db.Column(Text())
    descricao_auto:Mapped[str] = db.Column(Text())

    macros:Mapped[List['Macro']] = relationship(back_populates='micros')
    submacros:Mapped[List['Macro']] = relationship(back_populates='micros')

    def __init__(self, nome, panoid, origem, lat, long):
        self.nome = nome
        self.panoid = panoid
        self.origem = origem
        self.lat = lat
        self.long = long

    def __repr__(self):
        return f"<Micro {self.nome} em macros {[m.nome for m in self.macros]}>"