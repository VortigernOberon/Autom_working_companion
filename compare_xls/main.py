import tkinter as tk
from tkinter import filedialog, messagebox

# Importamos la función lógica (ahora sin pedir columna_clave)
from logica_excel import procesar_coincidencias

ruta_archivo1 = ""
ruta_archivo2 = ""

def seleccionar_archivo_1():
    global ruta_archivo1
    ruta = filedialog.askopenfilename(
        title="Selecciona el Primer Archivo Excel",
        filetypes=[("Archivos de Excel", "*.xlsx *.xls")]
    )
    if ruta:
        ruta_archivo1 = ruta
        etiqueta_archivo1.config(text=f"Archivo 1: {ruta.split('/')[-1]}", fg="blue")

def seleccionar_archivo_2():
    global ruta_archivo2
    ruta = filedialog.askopenfilename(
        title="Selecciona el Segundo Archivo Excel",
        filetypes=[("Archivos de Excel", "*.xlsx *.xls")]
    )
    if ruta:
        ruta_archivo2 = ruta
        etiqueta_archivo2.config(text=f"Archivo 2: {ruta.split('/')[-1]}", fg="blue")

def comparar():
    if not ruta_archivo1 or not ruta_archivo2:
        messagebox.showwarning("Faltan archivos", "Por favor, selecciona ambos archivos de Excel primero.")
        return

    ruta_guardado = filedialog.asksaveasfilename(
        title="Guardar archivos de resultados como (nombre base)...",
        defaultextension=".xlsx",
        filetypes=[("Archivo de Excel", "*.xlsx")]
    )
    
    if ruta_guardado:
        try:
            # Llamamos a la función enviando solo las rutas
            ruta_coin, ruta_dif = procesar_coincidencias(ruta_archivo1, ruta_archivo2, ruta_guardado)
            
            mensaje = (f"¡Archivos generados con éxito!\n\n"
                       f"Coincidencias (filas idénticas):\n{ruta_coin}\n\n"
                       f"Diferencias:\n{ruta_dif}")
            
            messagebox.showinfo("Proceso Terminado", mensaje)
            
        except ValueError as ve:
            messagebox.showwarning("Advertencia", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado al procesar:\n{e}")

# ==========================================
# INTERFAZ GRÁFICA
# ==========================================
ventana = tk.Tk()
ventana.title("Comparador de Archivos Excel - Documento Completo")
ventana.geometry("400x250") # Ventana más compacta ya que quitamos la entrada de texto

# Sección Archivo 1
tk.Button(ventana, text="Seleccionar Archivo 1", command=seleccionar_archivo_1).pack(pady=(20, 5))
etiqueta_archivo1 = tk.Label(ventana, text="Archivo 1: Ninguno", fg="gray")
etiqueta_archivo1.pack()

# Sección Archivo 2
tk.Button(ventana, text="Seleccionar Archivo 2", command=seleccionar_archivo_2).pack(pady=(15, 5))
etiqueta_archivo2 = tk.Label(ventana, text="Archivo 2: Ninguno", fg="gray")
etiqueta_archivo2.pack()

# Botón Principal
tk.Button(
    ventana, text="Comparar Documentos y Exportar", command=comparar, 
    bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"), padx=10, pady=5
).pack(pady=20)

ventana.mainloop()