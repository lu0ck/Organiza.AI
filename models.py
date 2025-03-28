from sqlalchemy import create_engine, Column, Integer, Float, Date, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuração do banco de dados SQLite
CONN = "sqlite:///bancodedados.db"
engine = create_engine(CONN, echo=True)
session = sessionmaker(bind=engine)()
base = declarative_base()

# Modelo para a tabela "Total Diário"
class TotalDiario(base):
    __tablename__ = "total_diario"
    id = Column(Integer, primary_key=True)
    data = Column(Date)          # Data do dia
    horario_saida = Column(String)  # Horário de saída (formato HH:MM)
    horario_chegada = Column(String) # Horário de chegada (formato HH:MM)
    km_total_dia = Column(Float) # Quilometragem total do dia
    ganho_total_dia = Column(Float) # Ganhos totais do dia
    gasto_total_abastecimento = Column(Float) # Gastos totais do dia com combustível
    gasto_total_alimentacao = Column(Float) # Gastos totais do dia com alimentação
    qtde_corridas = Column(Integer) # Quantidade de corridas realizadas no dia

# Modelo para a tabela "Corridas Individuais"
class Corrida(base):
    __tablename__ = "corridas"
    id = Column(Integer, primary_key=True)
    data = Column(Date)          # Data da corrida
    plataforma = Column(String)  # Plataforma (Uber, 99pop, Indrive)
    valor = Column(Float)        # Valor da corrida
    km = Column(Float)          # Quilometragem da corrida
    tempo = Column(Float)       # Tempo da corrida em minutos

# Cria as tabelas no banco de dados
base.metadata.create_all(engine)