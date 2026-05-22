import tkinter as tk

# Crear ventana
ventana = tk.Tk()
ventana.title("Hola Mundo")
ventana.geometry("300x200")

# Texto inicial
texto = tk.Label(ventana, text="Hola Mundo", font=("Arial", 20))
texto.pack(pady=30)

# Función para cambiar el texto
def cambiar_texto():
    texto.config(text="Adiós Mundo")

# Botón
boton = tk.Button(
    ventana,
    text="Presióname",
    command=cambiar_texto,
    font=("Arial", 14)
)

boton.pack()

# Ejecutar ventana
ventana.mainloop()
