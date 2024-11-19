from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import datetime

# Configuración de la base de datos
DATABASE_URL = "mysql+mysqlconnector://usuario:contraseña@localhost/cine"
# Reemplaza 'usuario' y 'contraseña' con los datos de tu base de datos

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definición del modelo de la tabla
class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    pelicula = Column(String(255), nullable=False)
    asiento = Column(String(10), nullable=False)
    horario = Column(DateTime, nullable=False)
    comprado = Column(Boolean, default=False)

# Crear la base de datos si no existe
Base.metadata.create_all(bind=engine)

# Inicialización de FastAPI
app = FastAPI()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rutas de la API

@app.post("/tickets/")
def crear_ticket(pelicula: str, asiento: str, horario: datetime.datetime, db: Session = Depends(get_db)):
    nuevo_ticket = Ticket(pelicula=pelicula, asiento=asiento, horario=horario)
    db.add(nuevo_ticket)
    db.commit()
    db.refresh(nuevo_ticket)
    return nuevo_ticket

@app.get("/tickets/")
def obtener_tickets(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tickets = db.query(Ticket).offset(skip).limit(limit).all()
    return tickets

@app.get("/tickets/{ticket_id}")
def obtener_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return ticket

@app.put("/tickets/{ticket_id}")
def actualizar_ticket(ticket_id: int, comprado: bool, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    ticket.comprado = comprado
    db.commit()
    return ticket

@app.delete("/tickets/{ticket_id}")
def eliminar_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    db.delete(ticket)
    db.commit()
    return {"message": "Ticket eliminado exitosamente"}
