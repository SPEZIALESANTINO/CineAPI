import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generar_pdf():
    nombre_pelicula = entry_pelicula.get()
    nombre_cliente = entry_cliente.get()

    if not nombre_pelicula or not nombre_cliente:
        messagebox.showerror("Error", "Por favor, complete todos los campos.")
        return

    # Crear el PDF
    nombre_archivo = f"{nombre_cliente}_ticket.pdf"
    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    c.drawString(100, 750, f"Ticket de Película")
    c.drawString(100, 730, f"Nombre del Cliente: {nombre_cliente}")
    c.drawString(100, 710, f"Película: {nombre_pelicula}")
    c.save()

    messagebox.showinfo("Éxito", f"PDF generado: {nombre_archivo}")

# Configuración de la ventana
ventana = tk.Tk()
ventana.title("Generador de Ticket de Película")

# Etiquetas y entradas
tk.Label(ventana, text="Nombre de la Película:").pack(pady=5)
entry_pelicula = tk.Entry(ventana, width=50)
entry_pelicula.pack(pady=5)

tk.Label(ventana, text="Nombre del Cliente:").pack(pady=5)
entry_cliente = tk.Entry(ventana, width=50)
entry_cliente.pack(pady=5)

# Botón para generar el PDF
btn_generar = tk.Button(ventana, text="Generar PDF", command=generar_pdf)
btn_generar.pack(pady=20)

# Ejecutar la ventana
ventana.mainloop()
