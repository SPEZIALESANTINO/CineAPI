from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

# Ruta para generar el PDF de un ticket
@app.get("/tickets/{ticket_id}/pdf")
def generar_pdf(ticket_id: int, db: Session = Depends(get_db)):
    # Buscar el ticket en la base de datos
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    # Nombre del archivo PDF
    pdf_file = f"ticket_{ticket_id}.pdf"

    # Crear el PDF
    c = canvas.Canvas(pdf_file, pagesize=A4)
    width, height = A4

    # Encabezado del PDF
    c.setFont("Helvetica-Bold", 18)
    c.drawString(100, height - 100, "Factura de Ticket de Cine")

    # Detalles del ticket
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 150, f"ID del Ticket: {ticket.id}")
    c.drawString(100, height - 170, f"Pelicula: {ticket.pelicula}")
    c.drawString(100, height - 190, f"Asiento: {ticket.asiento}")
    c.drawString(100, height - 210, f"Horario: {ticket.horario.strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(100, height - 230, f"Comprado: {'Sí' if ticket.comprado else 'No'}")

    # Pie de página
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(100, 50, "Gracias por su compra!")

    # Guardar el PDF
    c.save()

    # Enviar el archivo PDF como respuesta
    return FileResponse(
        path=pdf_file,
        filename=pdf_file,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={pdf_file}"}
    )
